
from generate_test_scenarios import generate_test_scenarios
from generate_test_cases import generate_test_cases
from add_code_execution import add_code_execution
from code_corrector import code_corrector
from helper import extract_python_code
from run_test_cases import write_and_run_test_file
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

    more_info="You are provided with an API endpoint. Change the query parmeters in the API endpoints to check for different users and also check whether there are any missing fields in the output schema or any field in the output schema is undefined"

    testscenarios=generate_test_scenarios(endpoint=endpoint, method=method, function_description=description, input_schema=input_schema, output_schema=output_schema, query_parameters=query_parameters, more_info=more_info)
    # data = json.loads(testscenarios)

    # test_scenarios = testscenarios["test_scenarios"]

    print(testscenarios)

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

    print("test cases generated")

    # resulttantcode=add_code_execution(test_code)

    # print("code execution added")

    corrected_code=code_corrector(test_code)

    print("code corrected")
    pcode=extract_python_code(corrected_code)

    write_and_run_test_file(pcode)