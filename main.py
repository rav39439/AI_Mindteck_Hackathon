
from generate_test_scenarios import generate_test_scenarios,generate_test_scenarios_input_schema,generate_test_scenarios_on_output_schema, generate_test_scenarios_more_information
from generate_test_cases import generate_test_cases,generate_test_cases_stepwise
from add_code_execution import add_code_execution
from code_corrector import code_corrector
from helper import extract_python_code
from run_test_cases import write_and_run_test_file,run_test_file
from analyze_final_results import analyze_result
import asyncio

def replace_pytest_fail(code: str) -> str:
    """
    Replaces all occurrences of pytest.fail() with print("testcase failed")
    
    Args:
        code (str): Python test code as a string
    
    Returns:
        str: Modified code
    """
    updated_code=code.replace("raise Exception", 'print')
    return code.replace("pytest.fail", 'print')



def generate_scenario_outputschema(
        
endpoint: str,
method: str,    
description: str,
output_schema,
query_parameters
):

    return generate_test_scenarios_on_output_schema(
    endpoint=endpoint,
    method=method,
    function_description=description,
    output_schema=output_schema,
    query_parameters=query_parameters,
    )

def generate_scenario_inputschema(
        
endpoint: str,
method: str,    
description: str,
input_schema,
query_parameters
):

    return generate_test_scenarios_input_schema(
    endpoint=endpoint,
    method=method,
    function_description=description,
    input_schema=input_schema,
    query_parameters=query_parameters,
    )

def generate_scenario_moreinfo(
        
endpoint: str,
method: str,    
description: str,
query_parameters,
more_info,
input_schema,
output_schema
):
    return generate_test_scenarios_more_information(
    endpoint=endpoint,
    method=method,
    function_description=description,
    input_schema=input_schema,
    output_schema=output_schema,
    query_parameters=query_parameters,
    more_info = more_info,
    
    )


def get_test_all_scenarios(
        
endpoint: str,
method: str,    
description: str,
query_parameters,
more_info,
input_schema,    
output_schema
):
    return generate_test_scenarios(
    endpoint=endpoint,
    method=method,
    function_description=description,
    input_schema=input_schema,
    output_schema=output_schema,
    query_parameters=query_parameters,
    more_info = more_info
    )


def isalltestexecution(testscenarios):
    test_code = generate_test_cases(
        endpoint=endpoint,
        method=method,
        function_description=description,
        input_schema=input_schema,
        output_schema=output_schema,
        query_parameters=query_parameters,
        more_info=more_info,
        test_scenarios=testscenarios
    )

    updated_code=replace_pytest_fail(test_code)
    corrected_code=code_corrector(test_code)
    updated_code=replace_pytest_fail(corrected_code)
    pcode=extract_python_code(updated_code)
    return pcode


def isalltestexecution_stepwise(testscenarios):
    all_test_scripts = []
    # Loop through each test scenario/test case
    for index, testcase in enumerate(testscenarios):
        # Generate test script for current testcase
        test_code = generate_test_cases_stepwise(
            index=index,
            endpoint=endpoint,
            method=method,
            function_description=description,
            input_schema=input_schema,
            output_schema=output_schema,
            query_parameters=query_parameters,
            more_info=more_info,
            test_scenarios=testcase   # passing one testcase at a time
        )

        print(f"Generated test case for: {testcase}")
        all_test_scripts.append(test_code)
        runner_function = """
        def run_test_functions():
            test_functions = [
                obj for name, obj in globals().items()
                if callable(obj) and name.startswith("test_")
            ]

            for test_func in test_functions:
                try:
                    print(f"Running: {test_func.__name__}")
                    test_func()
                    print("Testcase ran successfully")
                except Exception as e:
                    print("Testrun failed with error")

        if __name__ == "__main__":
            run_test_functions()
        """

    # final_test_script = "\n\n".join(all_test_scripts) + runner_function
    final_test_script = "\n\n".join(all_test_scripts)
    testswithadded_execution = add_code_execution(final_test_script)
    print("test cases generated")
    updated_code=replace_pytest_fail(testswithadded_execution)
    pcode=extract_python_code(updated_code)
    return pcode




def write_run_test_file_corr(pcode):
    return write_and_run_test_file(pcode)
    

    # return testscenarios1, testscenarios2, testscenarios3

if __name__ == "__main__":

    endpoint = "https://dummyjson.com/comments/add"
    method = "POST"
    description = "This api end point adds a new comment to the existing comments list"
    input_schema={
    "body": 'This makes all sense to me!',
    "postId": 3,
    "userId": 5,
  }
    output_schema = {
    "id": 341,
    "body": "This makes all sense to me!",
    "postId": 3,
    "user": {
        "id": 5,
        "username": "emmaj",
        "fullName": "Emma Miller"
  }
}
    
 
    query_parameters = ["userid"]

    more_info="You have to make sure that all the fields in nested field 'user' is validated and present. Make sure that all the fields in nested field 'user' is validated and present."
 
    # testscenarios=[{'description': 'Test with valid data and all fields present', 'outcome': 'API should pass', 'status': 200}, {'description': "Test with missing 'postId' field", 'outcome': 'API should fail', 'status': 400}, {'description': "Test with extra 'userId' query parameter", 'outcome': 'API should pass', 'status': 200}, {'description': "Test with invalid 'userId' query parameter (non-integer)", 'outcome': 'API should fail', 'status': 400}, {'description': "Test with incorrect 'postId' field value (negative)", 'outcome': 'API should fail', 'status': 400}, {'description': "Test with missing 'user' object in response", 'outcome': 'API should pass', 'status': 200}, {'description': "Test with missing 'fullName' field in 'user' object", 'outcome': 'API should pass', 'status': 200}, {'description': "Test with incorrect data type for 'body' field (non-string)", 'outcome': 'API should fail', 'status': 400}, {'description': "Test with nested 'user' object validation failure (missing 'id' field)", 'outcome': 'API should fail', 'status': 400}, {'description': "Test with nested 'user' object validation failure (invalid 'username' field value)", 'outcome': 'API should fail', 'status': 400}]
    testscenarios=generate_scenario_moreinfo(
        endpoint=endpoint,
        method=method,
        description=description,
        input_schema=input_schema,
        output_schema=output_schema,
        query_parameters=query_parameters,
        more_info=more_info
    )
    print(testscenarios)
    code_generated=isalltestexecution(testscenarios)
    result=write_run_test_file_corr(code_generated)
    print("fianl result")
    print(result)

    analysis=analyze_result(result,testscenarios)
    print(analysis)

#---------------------------------------------------------------------------------------------
    # run_test_file()



# AI Test Scenario & Testcase Generator Dashboard

## frontend/templates/index.html

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


class ScenarioConfig(BaseModel):
    scenario_type: str
    method: str
    execution_type: str
    functionality: str
    token: str


class ScenarioRequest(BaseModel):
    scenarios: str


class TestcaseRequest(BaseModel):
    testcases: str


class ResultRequest(BaseModel):
    results: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit-config")
async def submit_config(data: ScenarioConfig):

    scenarios = f"""
Generated scenarios based on:

Scenario Type: {data.scenario_type}
Method: {data.method}
Execution Type: {data.execution_type}
Functionality: {data.functionality}
"""

    return {
        "scenarios": scenarios
    }


@app.post("/add-scenario")
async def add_scenario(data: ScenarioRequest):

    updated = data.scenarios + "\n\nNew Scenario Added"

    return {
        "updated_scenarios": updated
    }


@app.post("/generate-testcases")
async def generate_testcases(data: ScenarioRequest):

    generated = f"""
Generated testcases for scenarios:

{data.scenarios}
"""

    return {
        "testcases": generated
    }


@app.post("/review-testcases")
async def review_testcases(data: TestcaseRequest):

    reviewed = data.testcases + "\n\n# Reviewed and corrected by AI"

    return {
        "reviewed_code": reviewed
    }


@app.post("/run-testcases")
async def run_testcases(data: TestcaseRequest):

    results = """
Testcase1 PASSED
Testcase2 FAILED
Testcase3 PASSED
"""

    return {
        "results": results
    }


@app.post("/generate-report")
async def generate_report(data: ResultRequest):

    report = f"""
Execution Report Generated Successfully

Summary:
{data.results}
"""

    return {
        "report": report
    }

# Run the async function
