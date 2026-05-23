from langchain_core.messages import HumanMessage, SystemMessage
import json
from llm import llm
from helper import clean_llm_output



def analyze_result(result, testscenarios,code):
    """
    Uses LLM to analyze test execution results and map failures back to scenarios.
    """

    system_prompt = SystemMessage(content="""
    You are an expert QA test result analyzer.

    Your job is to analyze:
    1. Test execution output (stdout/stderr)
    2. Original test scenarios

    You must identify:
    - Which scenarios passed
    - Which scenarios failed
    - Why they failed (based only on given result text)
    - Match failure messages to the correct scenario

    STRICT RULES:
    - Do NOT assume missing information
    - Use ONLY provided result and scenarios
    - Do NOT hallucinate errors not present in result
    - If mapping is unclear, mark scenario as "unknown failure"

    OUTPUT FORMAT MUST BE JSON ONLY:

    {
    "passed": ["scenario1", "scenario2"],
    "failed": [
        {
        "scenario": "scenario name/description",
        "reason": "exact reason from logs",
        "error_snippet": "relevant log snippet"
        }
    ],
    "unknown": []
    }

    Return ONLY JSON. No explanation. No markdown.
    """)

    user_prompt = HumanMessage(content=f"""
    TEST SCENARIOS:
    {testscenarios}

    EXECUTION CODE:
    {code}

    EXECUTION RESULT:
    {result}
    """)

    response = llm.invoke([system_prompt, user_prompt])

    cleaned = clean_llm_output(response.content)

    return cleaned


from langchain_core.messages import HumanMessage, SystemMessage
import json
from llm import llm
from helper import clean_llm_output


def generate_final_test_report(mapped_scenarios, std_output):
    """
    Uses LLM to combine:
    1. mapped testcase → scenario
    2. execution output (status_code + data)

    Returns structured final report WITHOUT PASS/FAIL evaluation.
    """

    system_prompt = SystemMessage(content="""
You are an expert QA test result aggregator.

You are given:
1. mapped_scenarios: mapping of testcase → scenario (description, outcome, status)
2. std_output: execution logs containing testcase results (status_code, data)

TASK:
- Match each testcase with its scenario
- Extract output (status_code + data)
- Combine everything into a structured report

STRICT RULES:
- Use ONLY provided inputs
- Do NOT assume missing testcases
- Do NOT hallucinate data
- If testcase is missing output, mark output as {}

OUTPUT FORMAT MUST BE JSON ONLY:

[
    {
        "testcase": "test_case_1",
        "scenario": {
            "description": "...",
            "outcome": "...",
            "status": 200
        },
        "output": {
            "status_code": 200,
            "data": {}
        }
    }
]

Return ONLY JSON.
No explanation.
No markdown.
""")

    user_prompt = HumanMessage(content=f"""
MAPPED SCENARIOS:
{json.dumps(mapped_scenarios, indent=2)}

STD OUTPUT:
{std_output}
""")

    response = llm.invoke([system_prompt, user_prompt])

    cleaned = clean_llm_output(response.content)

    try:
        return json.loads(cleaned)
    except Exception as e:
        return {
            "error": str(e),
            "raw_output": cleaned
        }
    



from langchain_core.messages import HumanMessage, SystemMessage
import json
from llm import llm
from helper import clean_llm_output


def map_testcases_to_scenarios(code_generated, testscenarios):
    """
    Uses LLM to map generated testcase functions with original test scenarios.
    Returns output in Python dictionary format with full scenario details.
    """

    system_prompt = SystemMessage(content="""
You are an expert QA testcase mapping analyzer.

Your task is to analyze:
1. Generated test code
2. Original test scenarios

You must identify which testcase function corresponds to which scenario.

STRICT RULES:
- Use ONLY provided test code and scenarios
- Do NOT assume missing mappings
- Match based on testcase logic, validation, assertions, payload, and behavior
- Every testcase function must be mapped to the closest matching scenario
- If mapping is unclear, return "unknown scenario"

IMPORTANT:
You MUST return COMPLETE scenario details including:
- description
- outcome
- status

OUTPUT FORMAT MUST BE VALID JSON ONLY:

{
    "test_case_1": {
        "description": "scenario description here",
        "outcome": "API should pass",
        "status": 200
    },

    "test_case_2": {
        "description": "another scenario",
        "outcome": "API should fail",
        "status": 400
    },

    "test_case_3": "unknown scenario"
}

Return ONLY JSON.
No explanation.
No markdown.
No extra text.
""")

    user_prompt = HumanMessage(content=f"""
TEST SCENARIOS:
{json.dumps(testscenarios, indent=2)}

GENERATED TEST CODE:
{code_generated}
""")

    response = llm.invoke([system_prompt, user_prompt])

    cleaned = clean_llm_output(response.content)

    try:
        # Convert JSON string into Python dict
        parsed_output = json.loads(cleaned)

        return parsed_output

    except Exception as e:
        return {
            "error": f"Failed to parse LLM output into dict: {e}",
            "raw_output": cleaned
        }

import re
import ast

import ast


def extract_testcase_results(output: str):
    """
    Production-grade testcase result extractor.

    Extracts:
    TestcaseX {'status_code': ..., 'data': {...}}

    Returns dictionary format.
    """

    result_dict = {}

    lines = output.splitlines()

    for line in lines:

        line = line.strip()

        # Skip irrelevant lines
        if not line.startswith("Testcase"):
            continue

        # Ignore pass/fail status lines
        if "passed" in line.lower() or "failed" in line.lower():
            continue

        try:
            # Split only at first space
            testcase_name, dict_part = line.split(" ", 1)

            # Convert string dict -> python dict
            parsed_data = ast.literal_eval(dict_part)

            result_dict[testcase_name] = parsed_data

        except Exception as e:

            result_dict[testcase_name] = {
                "error": f"Failed to parse data: {e}",
                "raw_line": line
            }

    return result_dict

# Example usage

import re


def normalize_name(name: str):
    """
    Normalizes:
    test_case_1 -> testcase1
    Testcase1 -> testcase1
    testcase-1 -> testcase1
    """

    if not name:
        return ""

    name = name.lower()

    digits = re.findall(r"\d+", name)

    if digits:
        return f"testcase{digits[0]}"

    return name.replace("_", "")


def merge_testcase_results(mapped_scenarios, extracted_results):
    """
    Robust merge of:
    - mapped scenarios
    - execution outputs
    """

    final_output = {}

    # Step 1: normalize extracted results once
    normalized_results = {
        normalize_name(k): v
        for k, v in extracted_results.items()
    }

    # Step 2: merge with scenarios
    for testcase_name, scenario in mapped_scenarios.items():

        norm_name = normalize_name(testcase_name)

        execution_output = normalized_results.get(norm_name)

        # fallback: try partial match if exact missing
        if execution_output is None:
            for k, v in normalized_results.items():
                if norm_name in k or k in norm_name:
                    execution_output = v
                    break

        if execution_output is None:
            execution_output = {}

        scenario_status = None
        if isinstance(scenario, dict):
            scenario_status = scenario.get("status")

        actual_status = None
        if isinstance(execution_output, dict):
            actual_status = execution_output.get("status_code")

        final_result = (
            "PASS"
            if actual_status is not None
            and scenario_status is not None
            and actual_status == scenario_status
            else "FAIL"
        )

        final_output[testcase_name] = {
            "name": testcase_name,
            "testcase": scenario,
            "output": execution_output,
            "final_result": final_result
        }

    return final_output


import json
import re

import json
import re

import json
import re


def clean_llm_json_output(raw_output):
    """
    Robust JSON cleaner for LLM outputs.
    Handles:
    - dict input with raw_output field
    - string input with noise
    - newline formatting
    - 'json\\n' prefix
    """

    # 🔥 STEP 0: if dict → extract raw_output first
    if isinstance(raw_output, dict):

        if "raw_output" in raw_output:
            raw_output = raw_output["raw_output"]
        else:
            return raw_output

    if raw_output is None:
        return {"error": "Empty output"}

    # Ensure string
    raw_output = str(raw_output)

    # 🔥 STEP 1: remove leading "json"
    cleaned = re.sub(r"^\s*json\s*", "", raw_output.strip(), flags=re.IGNORECASE)

    # 🔥 STEP 2: extract JSON block safely
    match = re.search(r"(\[.*\]|\{.*\})", cleaned, re.DOTALL)

    if not match:
        return {
            "error": "No JSON structure found",
            "raw_output": raw_output
        }

    json_str = match.group(1)

    # 🔥 STEP 3: parse JSON
    try:
        return json.loads(json_str)

    except json.JSONDecodeError:

        # cleanup common LLM issues
        json_str = re.sub(r",\s*}", "}", json_str)
        json_str = re.sub(r",\s*]", "]", json_str)

        try:
            return json.loads(json_str)

        except Exception as e:
            return {
                "error": str(e),
                "raw_output": raw_output
            }
data={'error': 'Expecting value: line 1 column 1 (char 0)', 'raw_output': 'json\n[\n    {\n        "testcase": "test_case_1",\n        "scenario": {\n            "description": "Test case: Adding a new comment with valid data",\n            "outcome": "API should pass",\n            "status": 201\n        },\n        "output": {\n            "status_code": 201,\n            "data": {\n                "id": 341,\n                "body": "This makes all sense to me!",\n                "postId": 3,\n                "user": {\n                    "id": 5,\n                    "username": "emmaj",\n                    "fullName": "Emma Miller"\n                }\n            }\n        },\n        "result": "PASS"\n    },\n    {\n        "testcase": "test_case_2",\n        "scenario": {\n            "description": "Test case: Adding a new comment with missing \'userId\'",\n            "outcome": "API should fail",\n            "status": 400\n        },\n        "output": {\n            "status_code": 400,\n            "data": {\n                "message": "User id is required"\n            }\n        },\n        "result": "FAIL"\n    },\n    {\n        "testcase": "test_case_3",\n        "scenario": {\n            "description": "Test case: Adding a new comment with invalid \'userId\' value",\n            "outcome": "API should fail",\n            "status": 400\n        },\n        "output": {\n            "status_code": 400,\n            "data": {\n                "message": "User id is required"\n            }\n        },\n        "result": "FAIL"\n    },\n    {\n        "testcase": "test_case_4",\n        "scenario": {\n            "description": "Test case: Adding a new comment with missing \'user\' field",\n            "outcome": "API should fail",\n            "status": 400\n        },\n        "output": {\n            "status_code": 201,\n            "data": {\n                "id": 341,\n                "body": "This makes all sense to me!",\n                "postId": 3,\n                "user": {\n                    "id": 5,\n                    "username": "emmaj",\n                    "fullName": "Emma Miller"\n                }\n            }\n        },\n        "result": "PASS"\n    },\n    {\n        "testcase": "test_case_5",\n        "scenario": {\n            "description": "Test case: Adding a new comment with missing \'fullName\' field in \'user\'",\n            "outcome": "API should fail",\n            "status": 400\n        },\n        "output": {\n            "status_code": 201,\n            "data": {\n                "id": 341,\n                "body": "This makes all sense to me!",\n                "postId": 3,\n                "user": {\n                    "id": 5,\n                    "username": "emmaj",\n                    "fullName": "Emma Miller"\n                }\n            }\n        },\n        "result": "PASS"\n    }\n]'}
result=clean_llm_json_output(data)




def evaluate_testcase_results(cleaned_output):
    """
    Updates result field based on:
    scenario.status == output.status_code
    """

    for item in cleaned_output:

        scenario_status = item.get("scenario", {}).get("status")
        output_status = item.get("output", {}).get("status_code")

        if scenario_status == output_status:
            item["result"] = "PASS"
        else:
            item["result"] = "FAIL"

    return cleaned_output
print(evaluate_testcase_results(result))
# scenarios=[{'description': 'Test case: Adding a new comment with valid data', 'outcome': 'API should pass', 'status': 201}, {'description': "Test case: Adding a new comment with missing 'userId'", 'outcome': 'API should fail', 'status': 400}, {'description': "Test case: Adding a new comment with invalid 'userId' value", 'outcome': 'API should fail', 'status': 400}, {'description': "Test case: Adding a new comment with missing 'user' field", 'outcome': 'API should fail', 'status': 400}, {'description': "Test case: Adding a new comment with missing 'fullName' field in 'user'", 'outcome': 'API should fail', 'status': 400}]

# code_generated=""
# with open("testcases.py", "r", encoding="utf-8") as f:
#     code_generated = f.read()

# r=map_testcases_to_scenarios(code_generated, scenarios)



# output = """
# Testcase1 {'status_code': 201, 'data': {'id': 341, 'body': 'This makes all sense to me!', 'postId': 3, 'user': {'id': 5, 'username': 'emmaj', 'fullName': 'Emma Miller'}}}
# Testcase1 passed
# Testcase2 {'status_code': 400, 'data': {'message': 'User id is required'}}
# Testcase2 passed
# Testcase3 {'status_code': 400, 'data': {'message': 'User id is required'}}
# Testcase3 passed
# Testcase4 {'status_code': 201, 'data': {'id': 341, 'body': 'This makes all sense to me!', 'postId': 3, 'user': {'id': 5, 'username': 'emmaj', 'fullName': 'Emma Miller'}}}
# Testcase4 failed: Expected status code 400 but got 201
# Testcase5 {'status_code': 201, 'data': {'id': 341, 'body': 'This makes all sense to me!', 'postId': 3, 'user': {'id': 5, 'username': 'emmaj', 'fullName': 'Emma Miller'}}}
# Testcase5 failed: Expected status code 400 but got 201
# """

# parsed = extract_testcase_results(output)


# # print(parsed)

# merged = merge_testcase_results(r, parsed)

# print(merged)
