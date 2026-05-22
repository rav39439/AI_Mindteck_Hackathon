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

    You are a QA engineer generating pytest test scripts for REST APIs.

    Use ONLY "Test Cases" as the source of test scripts generation logic.
                                          
    For each test case , Analyse the description , outcome and status code and generate test scripts .
                                          
    Make sure that test scripts should pass only for the status code mentioned in each test case.
                                          
    However, use Input Schema, Output Schema, Method, Endpoint only as supporting information to construct and validate the test scripts.
                                          
    Make sure that all the test scripts generated from test cases, are defined as separate functions. If needed, use pytest to structure them properly as individual test script.  
                                                                                  
    Make sure that you remove the pytest.fail and pytest.raises from the generated code.
                                          
    In the end add a function to execute all test scripts: def run_all_tests():
                                          
    In run_all_tests(): if you catch any exception then make sure you continue the execution of other test cases and dont raise any error
                                          
    call the function run_all_tests() at the end


    STRICT RULES:

    Each test script uses try/except
    Call API and use response.json() only after status_code check (e.g., 200)
    Make sure that all the test scripts are defined as separate functions
    Do NOT assume/fabricate endpoints, URLs, query params, or responses
    Do NOT generate or include pytest, pytest.mark.parametrize, globals(), dynamic invocation, or any custom test execution/wrapper functions under any condition.
    Only generate standalone test_case_* functions plus a single run_all_tests() that explicitly calls each test case sequentially with individual try/except blocks.
    Use ONLY given Endpoint (no modifications or additions)
    Validate only real response data (keys/types/status/values)
    pytest.fail, pytest.raises, or any pytest-based failure handling are strictly forbidden. All failures must be handled only using try/except blocks with print statements and re-raise.
    Name test scripts: test_case_1, test_case_2, ...
    except: print(f"Testcase{name} failed") then raise, also print one line mentioning name of testcase failed
    success: print("Testcase{name} passed")
    Make sure that run_all_tests() is defined at the end
    
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

    Test Cases:
    {json.dumps(test_scenarios, indent=2)}
"""
    )

    response = llm.invoke([system_prompt, user_prompt])

    cleaned = clean_llm_output(response.content)

    return cleaned




def generate_test_cases_stepwise(
    index:int,
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
    
    print(index)

    system_prompt=SystemMessage( content=("""

    You are a QA engineer generating pytest test scripts for REST APIs.

    Use ONLY "Test Case" in user prompt as the source of test script generation logic.
                                          
    You are provided a "Test Case" in the user prompt , Analyse the description , outcome and status code and generate test script for the given test case. 
                                          
    Make sure that test script should pass only for the status code mentioned in the Test case.
                                          
    However, use Input Schema, Output Schema, Method, Endpoint only as supporting information to construct and validate the Test Script.
                                          
    Make sure that test script is a python function without any argument. If needed, use pytest to structure them properly as test function.  
                                                                                  
    Make sure that you remove the pytest.fail and pytest.raises from the generated code.

    STRICT RULES:

    Each test script uses try/except
    except: print("Testcase{index} failed") then raise, also print one line mentioning name of testcase failed
    success: print("Testcase{index} passed")
    Do not run the test script.
    Call API and use response.json() only after status_code check (e.g., 200)
    Do NOT assume/fabricate endpoints, URLs, query params, or responses
    Use ONLY given Endpoint (no modifications or additions)
    Use only real response data (keys/types/status/values)
    pytest.fail, pytest.raises, or any pytest-based failure handling are strictly forbidden. All failures must be handled only using try/except blocks with print statements and re-raise.    
    Output ONLY Python code (no markdown/text)

"""))
# In the end add a function to execute the test script function: def run_test():
#     In run_test(): if you catch any exception then make sure you continue the execution of other test scripts and dont raise any error
#     call the function run_test() at the end
#     Name test scripts: test_case{index}

    user_prompt = HumanMessage(
        content=f"""
    Endpoint: {endpoint}
    
    Method: {method}

    Description:{function_description}

    Input Schema:
    {json.dumps(input_schema, indent=2)}

    Output Schema:
    {json.dumps(output_schema, indent=2)}

    Test Case:
    {json.dumps(test_scenarios, indent=2)}
"""
    )

    response = llm.invoke([system_prompt, user_prompt])

    cleaned = clean_llm_output(response.content)

    return cleaned

