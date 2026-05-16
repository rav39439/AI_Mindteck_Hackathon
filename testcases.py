import pytest
import requests

def test_case_1():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 5
        })
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data and 'body' in data and 'postId' in data and 'user_id' in data
    except Exception as e:
        print(f"Error: {e}")
        print("Testcase failed")

def test_case_2():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            "postId": 3,
            "userId": 5
        })
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data and 'body' in data and 'postId' in data and 'user_id' in data
    except Exception as e:
        print(f"Error: {e}")
        print("Testcase failed")

def test_case_3():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            "body": "This makes all sense to me!",
            "userId": 5
        })
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data and 'body' in data and 'postId' in data and 'user_id' in data
    except Exception as e:
        print(f"Error: {e}")
        print("Testcase failed")

def test_case_4():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            "body": "This makes all sense to me!",
            "postId": 3
        })
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data and 'body' in data and 'postId' in data and 'user_id' in data
    except Exception as e:
        print(f"Error: {e}")
        print("Testcase failed")

def test_case_5():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 999
        })
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data and 'body' in data and 'postId' in data and 'user_id' in data
    except Exception as e:
        print(f"Error: {e}")
        print("Testcase failed")

def test_case_6():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": -1
        })
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data and 'body' in data and 'postId' in data and 'user_id' in data
    except Exception as e:
        print(f"Error: {e}")
        print("Testcase failed")

def test_case_7():
    try:
        response = requests.post('https://dummyjson.com/comments/add', params={
            "userId": 4
        })
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data and 'body' in data and 'postId' in data and 'user_id' in data
    except Exception as e:
        print(f"Error: {e}")
        print("Testcase failed")

def test_case_8():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 5
        })
        data = response.json()
        assert 'id' in data and 'body' not in data['user']
    except Exception as e:
        print(f"Error: {e}")
        print("Testcase failed")

def test_case_9():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 5
        })
        data = response.json()
        assert 'id' in data and 'username' not in data['user']
    except Exception as e:
        print(f"Error: {e}")
        print("Testcase failed")

def run_all_tests():
    tests = [obj for obj in globals().values() if callable(obj) and obj.__name__.startswith('test_')]
    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except Exception as e:
            print(f"FAIL: {test.__name__} - Error: {e}")

if __name__ == "__main__":
    run_all_tests()