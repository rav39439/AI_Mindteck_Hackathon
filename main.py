
from generate_test_scenarios import generate_test_scenarios_input_schema,generate_test_scenarios_on_output_schema,generate_test_scenarios_more_information
from generate_test_cases import generate_test_cases
from add_code_execution import add_code_execution
from code_corrector import code_corrector
from helper import extract_python_code
from run_test_cases import write_and_run_test_file,run_test_file

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


import asyncio

# Wrapper to run blocking functions asynchronously
async def run_generate_test_scenarios(endpoint, method, description,
                                      input_schema, output_schema,
                                      query_parameters, more_info):

    task1 = asyncio.to_thread(
        generate_test_scenarios_more_information,
        endpoint=endpoint,
        method=method,
        function_description=description,
        input_schema=input_schema,
        output_schema=output_schema,
        query_parameters=query_parameters,
        more_info=more_info
    )

    task2 = asyncio.to_thread(
        generate_test_scenarios_on_output_schema,
        endpoint=endpoint,
        method=method,
        function_description=description,
        input_schema=input_schema,
        output_schema=output_schema,
        query_parameters=query_parameters,
        more_info=more_info
    )

    task3 = asyncio.to_thread(
        generate_test_scenarios_input_schema,
        endpoint=endpoint,
        method=method,
        function_description=description,
        input_schema=input_schema,
        output_schema=output_schema,
        query_parameters=query_parameters,
        more_info=more_info
    )

    # Run all concurrently
    testscenarios1, testscenarios2, testscenarios3 = await asyncio.gather(
        task1,
        task2,
        task3
    )

    

    return testscenarios1, testscenarios2, testscenarios3

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
    


#     query_parameters = ["userid"]

#     more_info="You have to make sure that all the fields in nested field 'user' is validated and present. Make sure that all the fields in nested field 'user' is validated and present."

#     testscenarios1, testscenarios2, testscenarios3 = asyncio.run(
#     run_generate_test_scenarios(
#         endpoint=endpoint,
#         method=method,
#         description=description,
#         input_schema=input_schema,
#         output_schema=output_schema,
#         query_parameters=query_parameters,
#         more_info=more_info
#     )
# )


#     merged_test_scenarios = (
#     (testscenarios1 or []) +
#     (testscenarios2 or []) +
#     (testscenarios3 or [])
# )    
   
#     print(merged_test_scenarios)
#     print(len(merged_test_scenarios))

    
#     test_code = generate_test_cases(
#         endpoint=endpoint,
#         method=method,
#         function_description=description,
#         input_schema=input_schema,
#         output_schema=output_schema,
#         query_parameters=query_parameters,
#         more_info=more_info,
#         test_scenarios=merged_test_scenarios
#     )

#     print("test cases generated")

#     print(test_code)

#     updated_code=replace_pytest_fail(test_code)

#     corrected_code=code_corrector(test_code)

#     updated_code=replace_pytest_fail(corrected_code)

#     print("code corrected")
#     pcode=extract_python_code(updated_code)

#     write_and_run_test_file(pcode)

    run_test_file()





# Run the async function
