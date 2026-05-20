from langchain_core.messages import HumanMessage, SystemMessage
import json
from llm import llm
from helper import clean_llm_output
# -----------------------------
# Generate Test Cases (Single Stage)
# -----------------------------
def generate_test_cases(
    endpoint: str,
    method: str,
    function_description: str,
    input_schema,
    output_schema,
    query_parameters=None,
    more_info:str="",
    test_scenarios=None
):
    if query_parameters is None:
        query_parameters = []
    
    print(more_info)

    system_prompt=SystemMessage( content=("""

    You are a QA engineer generating pytest tests for REST APIs.

    Use ONLY Test Scenarios as the source of test case generation logic.
                                          
    For each scenario , Analyse the description , outcome and status code and make sure that testcase should pass only for the status code mentioned in each scenario.
                                          
    However, use Input Schema, Output Schema, Method, Endpoint only as supporting information to construct and validate the test cases.
                                          
    Make sure that you remove the pytest.fail and pytest.raises from the generated code.

    STRICT RULES:

    Each test uses try/except
    except: print(f"Testcase{name} failed") then raise, also print one line mentioning name of testcase failed
    success: print("Testcase{name} passed")
    Call API and use response.json() only after status_code check (e.g., 200)
    Do NOT assume/fabricate endpoints, URLs, query params, or responses
    Use ONLY given Endpoint (no modifications or additions)
    Validate only real response data (keys/types/status/values)
    pytest.fail, pytest.raises, or any pytest-based failure handling are strictly forbidden. All failures must be handled only using try/except blocks with print statements and re-raise.
    Name tests: test_case_1, test_case_2, ...
    In the end add a function to execute all test cases: def run_all_tests():
    call the function run_all_tests() at the end
    Output ONLY Python code (no markdown/text)

"""))

    user_prompt = HumanMessage(
        content=f"""
    Endpoint: {endpoint}
    
    Method: {method}

    Input Schema:
    {json.dumps(input_schema, indent=2)}

    Output Schema:
    {json.dumps(output_schema, indent=2)}

    TEST SCENARIOS:
    {json.dumps(test_scenarios, indent=2)}
"""
    )

    response = llm.invoke([system_prompt, user_prompt])

    cleaned = clean_llm_output(response.content)

    return cleaned

