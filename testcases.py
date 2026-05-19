import requests
import json
import sys

def run_all_tests():
    test_cases = [
        {
            "description": "Test adding a new comment with valid input",
            "input_schema": {
                "body": "This makes all sense to me!",
                "postId": 3,
                "userId": 5
            },
            "output_schema": {
                "id": 341,
                "body": "This makes all sense to me!",
                "postId": 3,
                "user": {
                    "id": 5,
                    "username": "emmaj",
                    "fullName": "Emma Miller"
                }
            },
            "method": "POST",
            "endpoint": "https://dummyjson.com/comments/add",
            "status": 201
        },
        {
            "description": "Test adding a new comment with missing required field 'postId'",
            "input_schema": {
                "body": "This makes all sense to me!",
                "userId": 5
            },
            "output_schema": None,
            "method": "POST",
            "endpoint": "https://dummyjson.com/comments/add",
            "status": 400
        },
        {
            "description": "Test adding a new comment with extra unexpected field 'invalidField'",
            "input_schema": {
                "body": "This makes all sense to me!",
                "postId": 3,
                "userId": 5,
                "invalidField": "invalidValue"
            },
            "output_schema": None,
            "method": "POST",
            "endpoint": "https://dummyjson.com/comments/add",
            "status": 400
        },
        {
            "description": "Test adding a new comment with incorrect data type for 'body' or 'postId'",
            "input_schema": {
                "body": "This makes all sense to me!",
                "postId": 3,
                "userId": 5
            },
            "output_schema": None,
            "method": "POST",
            "endpoint": "https://dummyjson.com/comments/add",
            "status": 400
        },
        {
            "description": "Test adding a new comment with invalid value for 'userId'",
            "input_schema": {
                "body": "This makes all sense to me!",
                "postId": 3,
                "userId": -1
            },
            "output_schema": None,
            "method": "POST",
            "endpoint": "https://dummyjson.com/comments/add",
            "status": 201
        },
        {
            "description": "Test adding a new comment with boundary value for 'postId'",
            "input_schema": {
                "body": "This makes all sense to me!",
                "postId": 0,
                "userId": 5
            },
            "output_schema": None,
            "method": "POST",
            "endpoint": "https://dummyjson.com/comments/add",
            "status": 201
        },
        {
            "description": "Test adding a new comment with query parameter 'userid' set to 0",
            "input_schema": {
                "body": "This makes all sense to me!",
                "postId": 3,
                "userId": 0
            },
            "output_schema": None,
            "method": "POST",
            "endpoint": "https://dummyjson.com/comments/add?userid=0",
            "status": 400
        },
        {
            "description": "Test adding a new comment with query parameter 'userid' set to invalid value",
            "input_schema": {
                "body": "This makes all sense to me!",
                "postId": 3,
                "userId": "invalidValue"
            },
            "output_schema": None,
            "method": "POST",
            "endpoint": "https://dummyjson.com/comments/add?userid=invalidValue",
            "status": 400
        }
    ]

    for test_case in test_cases:
        try:
            response = requests.post(test_case["endpoint"], json=test_case["input_schema"])
            if response.status_code == test_case["status"]:
                print("Testcase passed")
            else:
                print(f"Error: {response.text}")
                raise Exception(f"Testcase failed for status code {test_case['status']}")
        except Exception as e:
            print(f"Error: {e}")

def run_all_tests():
    test_cases = [
        # ... (rest of the test cases)
    ]

    for test_case in test_cases:
        try:
            response = requests.post(test_case["endpoint"], json=test_case["input_schema"])
            if response.status_code == test_case["status"]:
                print("Testcase passed")
            else:
                print(f"Error: {response.text}")
                raise Exception(f"Testcase failed for status code {test_case['status']}")
        except Exception as e:
            print(f"Error: {e}")

    # Collect all test functions
    test_functions = [func for func in globals().values() if func.__name__.startswith("test_")]

    # Execute all tests
    for func in test_functions:
        try:
            func()
            print("Test passed")
        except Exception as e:
            print(f"Error: {e}")
            print("Test failed")

# Run the tests
run_all_tests()