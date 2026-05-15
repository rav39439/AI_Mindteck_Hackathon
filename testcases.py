import pytest
import requests

def test_case_1():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'body': "This makes all sense to me!",
            'postId': 3,
            'userId': 5
        })
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert 'id' in data
        assert 'body' in data
        assert 'postId' in data
        assert 'user' in data
        assert isinstance(data['user'], dict)
        assert 'id' in data['user']
        assert 'username' in data['user']
        assert 'fullName' in data['user']
    except Exception as e:
        print(f"Error: {e}")
        raise
def test_case_2():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'postId': 3,
            'userId': 5
        })
        assert response.status_code == 400
        data = response.json()
        assert isinstance(data, dict)
        assert 'error' in data
    except Exception as e:
        print(f"Error: {e}")
        raise

def test_case_3():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'postId': 3,
            'body': "This makes all sense to me!",
            'userId': 5
        })
        assert response.status_code == 400
        data = response.json()
        assert isinstance(data, dict)
        assert 'error' in data
        assert 'missingFields' in data
    except Exception as e:
        print(f"Error: {e}")
        raise

def test_case_4():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'postId': 3,
            'body': "This makes all sense to me!",
            'userId': 5
        })
        assert response.status_code == 400
        data = response.json()
        assert isinstance(data, dict)
        assert 'error' in data
        assert 'missingFields' in data
    except Exception as e:
        print(f"Error: {e}")
        raise

def test_case_5():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'postId': 3,
            'body': "This makes all sense to me!",
            'userId': 5
        })
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert 'id' in data
        assert 'body' in data
        assert 'postId' in data
        assert 'user' in data
        assert isinstance(data['user'], dict)
        assert 'id' not in data['user']
    except Exception as e:
        print(f"Error: {e}")
        raise

def test_case_6():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'body': "This makes all sense to me!",
            'postId': 3,
            'userId': 5
        }, params={'userid': 1})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert 'id' in data
        assert 'body' in data
        assert 'postId' in data
        assert 'user' in data
        assert isinstance(data['user'], dict)
        assert 'id' in data['user']
        assert 'username' in data['user']
        assert 'fullName' in data['user']
    except Exception as e:
        print(f"Error: {e}")
        raise

def test_case_7():
    try:
        response = requests.post('https://dummyjson.com/comments/add', json={
            'body': "This makes all sense to me!",
            'postId': 3,
            'userId': 5
        }, params={'userid': 2})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert 'id' in data
        assert 'body' in data
        assert 'postId' in data
        assert 'user' in data
        assert isinstance(data['user'], dict)
        assert 'id' in data['user']
        assert 'username' in data['user']
        assert 'fullName' in data['user']
    except Exception as e:
        print(f"Error: {e}")
        raise

def run_all_tests():
    tests = [test_case_1, test_case_2, test_case_3, test_case_4, test_case_5, test_case_6, test_case_7]
    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except Exception as e:
            print(f"FAIL: {test.__name__} - Error: {e}")

if __name__ == "__main__":
    run_all_tests()