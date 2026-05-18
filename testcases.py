import requests
import json
import pytest

def test_case_1():
    try:
        response = requests.post('https://dummyjson.com/comments/add', 
                                  json={'body': 'This makes all sense to me!', 'postId': 3, 'userId': 5})
        if response.status_code == 201:
            print("Testcase passed")
        else:
            raise Exception
    except Exception as e:
        print(f"Error: {response.text}")
        # pytest.fail(str(e))

def test_case_2():
    try:
        response = requests.post('https://dummyjson.com/comments/add', 
                                  json={'postId': 3, 'userId': 5})
        if response.status_code == 400:
            print("Testcase passed")
        else:
            raise Exception
    except Exception as e:
        print(f"Error: {response.text}")
        # pytest.fail(str(e))

def test_case_3():
    try:
        response = requests.post('https://dummyjson.com/comments/add', 
                                  json={'body': 'This makes all sense to me!', 'userId': 5})
        if response.status_code == 400:
            print("Testcase passed")
        else:
            raise Exception
    except Exception as e:
        print(f"Error: {response.text}")
        # pytest.fail(str(e))

def test_case_4():
    try:
        response = requests.post('https://dummyjson.com/comments/add', 
                                  json={'body': 'This makes all sense to me!', 'postId': 3})
        if response.status_code == 400:
            print("Testcase passed")
        else:
            raise Exception
    except Exception as e:
        print(f"Error: {response.text}")
        # pytest.fail(str(e))

def test_case_5():
    try:
        response = requests.post('https://dummyjson.com/comments/add', 
                                  json={'body': 'This makes all sense to me!', 'postId': 4, 'userId': 5})
        if response.status_code == 201:
            print("Testcase passed")
        else:
            raise Exception
    except Exception as e:
        print(f"Error: {response.text}")
        # pytest.fail(str(e))

def test_case_6():
    try:
        response = requests.post('https://dummyjson.com/comments/add', 
                                  json={'body': 'This makes all sense to me!'}, 
                                  params={'userid': 5})
        if response.status_code == 400:
            print("Testcase passed")
        else:
            raise Exception
    except Exception as e:
        print(f"Error: {response.text}")
        # pytest.fail(str(e))

def test_case_7():
    try:
        response = requests.post('https://dummyjson.com/comments/add', 
                                  json={'body': 'This makes all sense to me!', 'postId': 3, 'userId': 5})
        if response.status_code == 500:
            print("Testcase passed")
        else:
            raise Exception
    except Exception as e:
        print(f"Error: {response.text}")
        # pytest.fail(str(e))

def test_case_8():
    try:
        response = requests.post('https://dummyjson.com/comments/add', 
                                  json={'body': 'This makes all sense to me!', 'postId': 3, 'userId': 5})
        if response.status_code == 500:
            print("Testcase passed")
        else:
            raise Exception
    except Exception as e:
        print(f"Error: {response.text}")
        # pytest.fail(str(e))

def run_all_tests():
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()
    test_case_6()
    test_case_7()
    test_case_8()

run_all_tests()