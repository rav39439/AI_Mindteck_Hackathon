
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
       Use only: API Description, Method, Endpoint, Input Schema, Output Schema, More Info provided in user_prompt.

Use More Info provided in user-prompt to derive additional edge cases and testcases.

You must generate comprehensive testcases covering BOTH input schema validation and output schema contract validation. Neither schema may be ignored.

Generate testcases by modifying the input schema only for POST/PUT requests (add, remove, or update fields). All modifications must remain realistic and consistent with API behavior. Include scenarios for missing required fields, extra unexpected fields, incorrect data types, invalid values, boundary values, and query parameter variations if supported.

Generate testcases on output schema  that validate the API response structure including missing fields, extra fields, incorrect field names (case-sensitive), incorrect data types, incorrect nesting, and contract mismatches. If nested fields are present, you must explicitly identify them and generate separate scenarios validating each nested object and its internal fields.

You must generate as many testcases as possible based on input schema and output schema.

Do not assume hidden fields, undocumented rules, schema definitions, or implicit validations.

Write testcases in simple English only.

Rules:
Do not assume anything not provided.
Do not modify the method and endpoint provided in user prompt.
You must generate testcases on both input and output schema with clear distribution.
You must generate testcases on "More Info" in the user prompt.
You must explicitly identify and validate nested fields in the output schema if present.
In each testcases, clearly describe how the API should behave and whether it should pass or fail.
Status code must logically match the expected outcome based on the testcases.
Modify query parameters only if required and supported.
Input schema changes allowed only for POST/PUT APIs.

Output must be valid JSON only in this format:

[
{"description":"testcase description here",
"outcome":"API should pass or fail",
"status":proper status code based on outcome and description"
},

{
"description":"Another testcase description here",
"outcome":"API should pass or fail",
"status":proper status code based on outcome and description"
}
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




def generate_test_scenarios_more_information(
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
       Use only: "Description", "Method",Input Schema, Output Schema, "Endpoint" and "More Info" provided in user_prompt.

"More Info" in user prompt is the primary source of test cases generation.

"Analyze the {more_info} provided in user prompt before generating the testcases."

use Input Schema, Output Schema, Method, Endpoint only as supporting information in generating the test cases.

Write test cases in simple English only.

Rules:
Do not assume anything not provided.
Do not modify the method and endpoint provided in user prompt.
You must generate test cases on "More Info" in the user prompt.
In each scenario, clearly describe how the API should behave and whether it should pass or fail.
Status code must logically match the expected outcome based on the scenario.
Modify query parameters only if required and supported.
Output must be valid JSON only in this format:

[
{"description":"test case description here",
"outcome":"API should pass or fail",
"status":proper status code based on outcome and description"
},

{"description":"Another test case description here",
"outcome":"API should pass or fail",
"status":proper status code based on outcome and description"
}
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

    Query Parameters:
    {json.dumps(query_parameters, indent=2)}

    Input Schema:
    {json.dumps(input_schema, indent=2)}

    Output Schema:
    {json.dumps(output_schema, indent=2)}

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




def generate_test_scenarios_input_schema(
    endpoint: str,
    method: str,
    function_description: str,
    input_schema,
    query_parameters=None,
   
):
    if query_parameters is None:
        query_parameters = []

    system_prompt = SystemMessage(
        content="""
       Use only:"Description", "Method", "Endpoint", "Input Schema" provided in user_prompt.

Generate test cases by modifying the input schema only for POST/PUT requests (add, remove, or update fields). All modifications must remain realistic and consistent with API behavior. Include scenarios for missing required fields, extra unexpected fields, incorrect data types, invalid values, boundary values, and query parameter variations if supported.

Also Generate test cases on input schema validation.

You must generate as many test cases as possible based on input schema.

Do not assume hidden fields, undocumented rules, schema definitions, or implicit validations.

Write test cases in simple English only.

Rules:
Do not assume anything not provided.
Do not modify the method and endpoint provided in user prompt.
You must generate scenarios only input schema with clear distribution.
In each test case, clearly describe how the API should behave and whether it should pass or fail.
Status code must logically match the expected outcome based on the scenario.
Modify query parameters only if required and supported.
Input schema changes allowed only for POST/PUT APIs.

Output must be valid JSON only in this format:

[
{"description":"test case description here",
"outcome":"API should pass or fail",
"status":proper status code based on outcome and description"
},

{"description":"Another test case description here",
"outcome":"API should pass or fail",
"status":proper status code based on outcome and description"
}
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


    Query Parameters:
    {json.dumps(query_parameters, indent=2)}

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



def generate_test_scenarios_on_output_schema(
    endpoint: str,
    method: str,
    function_description: str,
    output_schema,
    query_parameters=None,
):
    if query_parameters is None:
        query_parameters = []

    system_prompt = SystemMessage(
        content="""
       Use only: "Description", "Method", "Endpoint" and "Output Schema" provided in user_prompt.

You must generate comprehensive test cases covering ONLY on output schema.

Generate test cases on output schema  that validate the API response structure including missing fields, extra fields, incorrect field names (case-sensitive), incorrect data types, incorrect nesting, and contract mismatches. If nested fields are present, you must explicitly identify them and generate separate scenarios validating each nested object and its internal fields.

You must generate as many test cases as possible based on output schema.

Do not assume hidden fields, undocumented rules, schema definitions, or implicit validations.

Write test cases in simple English only.

Rules:
Do not assume anything not provided.
Do not modify the method and endpoint provided in user prompt.
You must generate test cases on output schema with clear distribution.
You must explicitly identify and validate nested fields in the output schema if present.
In each test case, clearly describe how the API should behave and whether it should pass or fail.
Status code must logically match the expected outcome based on the test case.
Modify query parameters only if required and supported.

Output must be valid JSON only in this format:

[
{"description":"test case description here",
"outcome":"API should pass or fail",
"status":proper status code based on outcome and description"
},

{"description":"Another test case description here",
"outcome":"API should pass or fail",
"status":proper status code based on outcome and description"
}
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

    Output Schema:
    {json.dumps(output_schema, indent=2)}

    Query Parameters:
    {json.dumps(query_parameters, indent=2)}

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
