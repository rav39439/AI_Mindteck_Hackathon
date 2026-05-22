import requests
import json
import pytest

def test_case_1():
    try:
        data = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 5
        }
        response = requests.post('https://dummyjson.com/comments/add', json=data)
        assert response.status_code == 201
        response_json = response.json()
        expected_output = {
            "id": 341,
            "body": "This makes all sense to me!",
            "postId": 3,
            "user": {
                "id": 5,
                "username": "emmaj",
                "fullName": "Emma Miller"
            }
        }
        assert response_json == expected_output
        print("Testcase1 passed")
    except Exception as e:
        print(f"Testcase1 failed: {str(e)}")

def test_case_2():
    try:
        data = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": None
        }
        response = requests.post('https://dummyjson.com/comments/add', json=data)
        assert response.status_code == 400
        print("Testcase2 passed")
    except Exception as e:
        print(f"Testcase2 failed: {str(e)}")

def test_case_3():
    try:
        data = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 12345
        }
        response = requests.post('https://dummyjson.com/comments/add', json=data)
        assert response.status_code == 400
        print("Testcase3 passed")
    except Exception as e:
        print(f"Testcase3 failed: {str(e)}")

def test_case_4():
    try:
        data = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 5
        }
        del data["user"]
        response = requests.post('https://dummyjson.com/comments/add', json=data)
        assert response.status_code == 400
        print("Testcase4 passed")
    except Exception as e:
        print(f"Testcase4 failed: {str(e)}")

def test_case_5():
    try:
        data = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 5
        }
        del data["user"]["fullName"]
        response = requests.post('https://dummyjson.com/comments/add', json=data)
        assert response.status_code == 400
        print("Testcase5 passed")
    except Exception as e:
        print(f"Testcase5 failed: {str(e)}")

def run_all_tests():
    test_functions = [test_case_1, test_case_2, test_case_3, test_case_4, test_case_5]
    for func in test_functions:
        try:
            func()
        except Exception as e:
            print(f"Testcase failed: {str(e)}")

if __name__ == "__main__":
    run_all_tests()