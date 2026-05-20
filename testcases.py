import requests
import json
import sys
import os

def test_case_1():
    
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'body': "This makes all sense to me!",
            'postId': 3,
            'userId': 5
        })
        assert response.status_code == 201
        print("Testcase 1 passed")
    except Exception as e:
        print(f"Testcase 1 failed: {e}")

def test_case_2():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'body': "",
            'postId': 3,
            'userId': 5
        })
        assert response.status_code == 400
        print("Testcase 2 passed")
    except Exception as e:
        print(f"Testcase 2 failed: {e}")

def test_case_3():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'body': "This makes all sense to me!",
            'postId': '3',
            'userId': 5
        })
        assert response.status_code == 400
        print("Testcase 3 passed")
    except Exception as e:
        print(f"Testcase 3 failed: {e}")

def test_case_4():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'body': "This makes all sense to me!",
            'postId': 3,
            'userId': 0
        })
        assert response.status_code == 400
        print("Testcase 4 passed")
    except Exception as e:
        print(f"Testcase 4 failed: {e}")

def test_case_5():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'body': "This makes all sense to me!",
            'postId': 3,
            'userId': 5,
            'extraField': 'extraValue'
        })
        assert response.status_code == 400
        print("Testcase 5 passed")
    except Exception as e:
        print(f"Testcase 5 failed: {e}")

def test_case_6():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'postId': 3,
            'userId': 5
        })
        assert response.status_code == 400
        print("Testcase 6 passed")
    except Exception as e:
        print(f"Testcase 6 failed: {e}")

def test_case_7():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'postId': 3,
            'userId': 5,
            'userid': '123'
        })
        assert response.status_code == 400
        print("Testcase 7 passed")
    except Exception as e:
        print(f"Testcase 7 failed: {e}")

def test_case_8():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'postId': 3,
            'userId': 5,
            'username': ''
        })
        assert response.status_code == 400
        print("Testcase 8 passed")
    except Exception as e:
        print(f"Testcase 8 failed: {e}")

def test_case_9():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'postId': 3,
            'userId': 5,
            'fullName': 'a'
        })
        assert response.status_code == 400
        print("Testcase 9 passed")
    except Exception as e:
        print(f"Testcase 9 failed: {e}")

def test_case_10():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'postId': 3,
            'userId': 5,
            'id': '123'
        })
        assert response.status_code == 400
        print("Testcase 10 passed")
    except Exception as e:
        print(f"Testcase 10 failed: {e}")


def run_all_tests():
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()
    test_case_6()
    test_case_7()
    test_case_8()
    test_case_9()
    test_case_10()

    # tests = globals().copy()
    # for key in list(tests.keys()):
    #     if key.startswith('test_'):
    #         del tests[key]
    
    # test_functions = [key for key in tests.keys() if key.startswith('test_')]
    # try:
    #     for func in test_functions:
    #         func()
    #     print("All tests passed")
    # except Exception as e:
    #     print(f"All tests failed: {e}")

if __name__ == "__main__":
    run_all_tests()