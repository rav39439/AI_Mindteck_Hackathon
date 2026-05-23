import requests
import json
import pytest

def test_case_1():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 5
        })
        print("test_case_1:", {
            "status_code": response.status_code,
            "data": response.json()
        })
        assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
    except Exception as e:
        print(f"Testcase{e.__name__} failed")

def test_case_2():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": None
        })
        print("test_case_2:", {
            "status_code": response.status_code,
            "data": response.json()
        })
        assert response.status_code == 400, f"Expected status code 400 but got {response.status_code}"
    except Exception as e:
        print(f"Testcase{e.__name__} failed")

def test_case_3():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 12345
        })
        print("test_case_3:", {
            "status_code": response.status_code,
            "data": response.json()
        })
        assert response.status_code == 400, f"Expected status code 400 but got {response.status_code}"
    except Exception as e:
        print(f"Testcase{e.__name__} failed")

def test_case_4():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 5
        })
        print("test_case_4:", {
            "status_code": response.status_code,
            "data": response.json()
        })
        assert 'user' not in response.json(), f"Expected 'user' field to be missing but got {response.json()}"
    except Exception as e:
        print(f"Testcase{e.__name__} failed")

def test_case_5():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 5
        })
        print("test_case_5:", {
            "status_code": response.status_code,
            "data": response.json()
        })
        assert 'fullName' not in response.json()['user'], f"Expected 'fullName' field to be missing but got {response.json()}"
    except Exception as e:
        print(f"Testcase{e.__name__} failed")

def run_all_tests():
    test_cases = [test_case_1, test_case_2, test_case_3, test_case_4, test_case_5]
    for test in test_cases:
        try:
            test()
            print("PASS")
        except Exception as e:
            print(f"FAIL: {e}")

if __name__ == "__main__":
    run_all_tests()