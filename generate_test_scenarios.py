
from langchain_core.messages import HumanMessage, SystemMessage
import json
import re
from llm import llm,llm_scenarios


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
    API Description, Method, Endpoint, Input Schema, Output Schema, More Info provided in user_prompt.

    Generate multiple test scenarios ensuring good coverage of different cases. Generate multiplescenarios on different categories (schema validation, contract validation, negative cases, boundary cases, and other relevant scenarios derived strictly from the provided information).

    Use More Info provided in user-prompt  to derive additional edge cases and test scenarios.

    Input modification rules: Query parameters may be modified freely. Input schema may be modified only for POST/PUT requests (add, remove, or update fields). All modifications must remain realistic and consistent with API behavior.

    Strict assertion rules: No keyword-only assertions are allowed. Every assertion must be a complete executable validation statement. Schema references, $ref, and schema paths are strictly prohibited.

    Output Schema rules: Output Schema is a strict contract. No missing fields, no extra fields, exact field names (case-sensitive), and exact nesting must be preserved. Schema validation must include strict checks for missing fields, extra fields, and type mismatches.

    Do not assume hidden fields, undocumented rules, schema definitions, or implicit validations.

    Write scenarios in simple English only.


    Rules:
    Do not assume anything not provided.
    Do not modify the method and endpoint provided in user prompt.
    Do not use code, assertions, operators (>, <, ===, etc.).
    Do not fabricate fields, endpoints, or responses.
    Describe data conceptually only.
    In each scenario that you generated above ,you must describe how API should behave as outcome of scenario.The behaviour should indicate whether api should pass and fail. Use your own logic in determining whether the API should pass or fail.
    Modify query parameters only if required and supported.
    Input schema changes allowed only for POST/PUT APIs.
    Do not include numbers, prefixes, labels, or category names.
    Each scenario must be a single-line sentence.
    Do not insert newline characters inside a scenario.

    Output must be valid JSON only in this format:

    [
    {"description":"Scenario description here",
    "outcome":"API should pass or fail",
    "status":proper status code based on outcome and description"
    },

    {"description":"Another Scenario description here",
    "outcome":"API should pass or fail",
    "status":proper status code based on outcome and description"
    },

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

    response = llm_scenarios.invoke([system_prompt, user_prompt])

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
