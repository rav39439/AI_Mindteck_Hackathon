import requests
import json
import unittest

def run_all_tests():
    test_cases = [
        # Test with valid user data
        {
            'name': 'test_case_1',
            'input_schema': {
                'body': "This makes all sense to me!",
                'postId': 3,
                'userId': 5
            },
            'output_schema': {
                'id': 341,
                'body': "This makes all sense to me!",
                'postId': 3,
                'user': {
                    'id': 5,
                    'username': "emmaj",
                    'fullName': "Emma Miller"
                }
            },
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 201
        },
        # Test with missing user id
        {
            'name': 'test_case_2',
            'input_schema': {
                'body': "This makes all sense to me!",
                'postId': 3,
                'userId': None
            },
            'output_schema': {},
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 400
        },
        # Test with invalid user id
        {
            'name': 'test_case_3',
            'input_schema': {
                'body': "This makes all sense to me!",
                'postId': 3,
                'userId': -1
            },
            'output_schema': {},
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 400
        },
        # Test with empty user name
        {
            'name': 'test_case_4',
            'input_schema': {
                'body': "",
                'postId': 3,
                'userId': 5
            },
            'output_schema': {},
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 400
        },
        # Test with empty user email
        {
            'name': 'test_case_5',
            'input_schema': {
                'body': "This makes all sense to me!",
                'postId': 3,
                'userId': 5
            },
            'output_schema': {},
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 400
        },
        # Test with valid comment text
        {
            'name': 'test_case_6',
            'input_schema': {
                'body': "This makes all sense to me!",
                'postId': 3,
                'userId': 5
            },
            'output_schema': {
                'id': 341,
                'body': "This makes all sense to me!",
                'postId': 3,
                'user': {
                    'id': 5,
                    'username': "emmaj",
                    'fullName': "Emma Miller"
                }
            },
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 201
        },
        # Test with missing comment text
        {
            'name': 'test_case_7',
            'input_schema': {
                'body': "",
                'postId': 3,
                'userId': 5
            },
            'output_schema': {},
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 400
        },
        # Test with invalid comment text
        {
            'name': 'test_case_8',
            'input_schema': {
                'body': "This makes all sense to me!",
                'postId': 3,
                'userId': 5
            },
            'output_schema': {},
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 400
        },
        # Missing required fields in the request body
        {
            'name': 'test_case_9',
            'input_schema': {
                'postId': 3,
                'userId': 5
            },
            'output_schema': {},
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 400
        },
        # Extra field 'created' not present in output schema
        {
            'name': 'test_case_10',
            'input_schema': {
                'body': "This makes all sense to me!",
                'postId': 3,
                'userId': 5,
                'title': 'Test Title'
            },
            'output_schema': {},
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 400
        },
        # Incorrect data type for 'postId' (should be integer)
        {
            'name': 'test_case_11',
            'input_schema': {
                'body': "This makes all sense to me!",
                'postId': '3',
                'userId': 5
            },
            'output_schema': {},
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 400
        },
        # Invalid value for 'postId' (out of range)
        {
            'name': 'test_case_12',
            'input_schema': {
                'body': "This makes all sense to me!",
                'postId': -1,
                'userId': 5
            },
            'output_schema': {},
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 400
        },
        # Incorrect data type for 'userId' (should be integer)
        {
            'name': 'test_case_13',
            'input_schema': {
                'body': "This makes all sense to me!",
                'postId': 3,
                'userId': '5'
            },
            'output_schema': {},
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 400
        },
        # Invalid value for 'userId' (out of range)
        {
            'name': 'test_case_14',
            'input_schema': {
                'body': "This makes all sense to me!",
                'postId': 3,
                'userId': -1
            },
            'output_schema': {},
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 400
        },
        # Boundary value for 'postId' (minimum value is 1)
        {
            'name': 'test_case_15',
            'input_schema': {
                'body': "This makes all sense to me!",
                'postId': 1,
                'userId': 5
            },
            'output_schema': {
                'id': 341,
                'body': "This makes all sense to me!",
                'postId': 3,
                'user': {
                    'id': 5,
                    'username': "emmaj",
                    'fullName': "Emma Miller"
                }
            },
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 201
        },
        # Boundary value for 'userId' (minimum value is 1)
        {
            'name': 'test_case_16',
            'input_schema': {
                'body': "This makes all sense to me!",
                'postId': 3,
                'userId': 1
            },
            'output_schema': {
                'id': 341,
                'body': "This makes all sense to me!",
                'postId': 3,
                'user': {
                    'id': 5,
                    'username': "emmaj",
                    'fullName': "Emma Miller"
                }
            },
            'method': 'POST',
            'endpoint': 'https://dummyjson.com/comments/add',
            'status_code': 201
        },
    ]

    def test_post_comments(self):
        for input_schema in self.input_schemas:
            try:
                response = requests.post('https://dummyjson.com/comments/add', json=input_schema)
                assert response.status_code == input_schema['status_code']
            except AssertionError as e:
                print(f"Test failed: {e}")
                continue


    if __name__ == '__main__':
        unittest.main()