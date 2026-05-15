
from langchain_core.messages import HumanMessage, SystemMessage
import json
import re
from llm import llm


def generate_test_scenarios(
    endpoint: str,
    method: str,
    function_description: str,
    input_schema,
    output_schema,
    query_parameters=None,
    more_info: str = ""
):
    if query_parameters is None:
        query_parameters = []

    system_prompt = SystemMessage(
        content="""
     
   
 Use only:
API Description, Method, Endpoint, Input Schema, Output Schema, More Info.

Generate multiple test scenarios ensuring good coverage of different cases. Aim for at least 1–2 scenarios per logical category when possible (schema validation, contract validation, negative cases, boundary cases, and other relevant scenarios derived strictly from the provided information).

Write scenarios in simple English only.

Rules:
Do not assume anything not provided.
Do not use code, assertions, operators (>, <, ===, etc.).
Do not fabricate fields, endpoints, or responses.
Describe data conceptually only.
Modify query parameters only if required and supported.
Input schema changes allowed only for POST/PUT APIs.
Do not include numbers, prefixes, labels, or category names.
Each scenario must be a single-line sentence.
Do not insert newline characters inside a scenario.
Do not use bullet points.

Output must be valid JSON only in this format:

[
"Scenario description here",
"Another scenario description here"
]

Return ONLY the JSON array.
No explanation.
No markdown.
No extra text.

"""
    )
    user_prompt = HumanMessage(
        content=f"""
    Endpoint: {endpoint}
    Method: {method}

    Description:
    {function_description}

    Input Schema:
    {json.dumps(input_schema, indent=2)}

    Output Schema:
    {json.dumps(output_schema, indent=2)}

    Query Parameters:
    {json.dumps(query_parameters, indent=2)}

    More Info:
    {more_info}
"""
    )

    response = llm.invoke([system_prompt, user_prompt])

    raw_output = response.content.strip()

    # Clean accidental markdown if present
    raw_output = raw_output.replace("```json", "").replace("```", "").strip()

    try:
        parsed_json = json.loads(raw_output)
    except json.JSONDecodeError:
        print("Invalid JSON returned by LLM:")
        print(raw_output)
        raise

    return parsed_json
