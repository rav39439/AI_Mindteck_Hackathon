def test_adding_new_comment_with_valid_input():
    import requests
    import json

    def run_test():
        endpoint = "https://dummyjson.com/comments/add"
        input_schema = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 5
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

        response = requests.post(endpoint, json=input_schema)
        assert response.status_code == 201
        assert response.json() == output_schema

    run_test()

def test_adding_new_comment_with_missing_required_field_post():
    import requests
    import json

    def run_test():
        endpoint = "https://dummyjson.com/comments/add"
        input_schema = {
            "body": "This makes all sense to me!",
            "userId": 5
        }
        output_schema = None

        response = requests.post(endpoint, json=input_schema)
        assert response.status_code == 400
        assert response.json() is not None

    run_test()

def test_adding_new_comment_with_extra_unexpected_field_post():
    import requests
    import json

    def run_test():
        endpoint = "https://dummyjson.com/comments/add"
        input_schema = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 5,
            "invalidField": "invalidValue"
        }
        output_schema = None

        response = requests.post(endpoint, json=input_schema)
        assert response.status_code == 400
        assert response.json() is not None

    run_test()

def test_adding_new_comment_with_incorrect_data_type_for_body_or_postid():
    import requests
    import json

    def run_test():
        endpoint = "https://dummyjson.com/comments/add"
        input_schema = {
            "body": 123,
            "postId": 3,
            "userId": 5
        }
        output_schema = None

        response = requests.post(endpoint, json=input_schema)
        assert response.status_code == 400
        assert response.json() is not None

    run_test()

def test_adding_new_comment_with_invalid_value_for_user_id():
    import requests
    import json

    def run_test():
        endpoint = "https://dummyjson.com/comments/add"
        input_schema = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": -1
        }
        output_schema = None

        response = requests.post(endpoint, json=input_schema)
        assert response.status_code == 201
        assert response.json() is not None

    run_test()

def test_adding_new_comment_with_boundary_value_for_postid():
    import requests
    import json

    def run_test():
        endpoint = "https://dummyjson.com/comments/add"
        input_schema = {
            "body": "This makes all sense to me!",
            "postId": 0,
            "userId": 5
        }
        output_schema = None

        response = requests.post(endpoint, json=input_schema)
        assert response.status_code == 201
        assert response.json() is not None

    run_test()

def test_adding_new_comment_with_query_parameter_userid_set_to_0():
    import requests
    import json

    def run_test():
        endpoint = "https://dummyjson.com/comments/add?userid=0"
        input_schema = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 0
        }
        output_schema = None

        response = requests.post(endpoint, json=input_schema)
        assert response.status_code == 400
        assert response.json() is not None

    run_test()

def test_adding_new_comment_with_query_parameter_userid_set_to_invalid_value():
    import requests
    import json

    def run_test():
        endpoint = "https://dummyjson.com/comments/add?userid=invalidValue"
        input_schema = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": "invalidValue"
        }
        output_schema = None

        response = requests.post(endpoint, json=input_schema)
        assert response.status_code == 400
        assert response.json() is not None

    run_test()

# Run the tests
import unittest
class TestCommentAddition(unittest.TestCase):
    def test_adding_new_comment_with_valid_input(self):
        import requests
        import json

        endpoint = "https://dummyjson.com/comments/add"
        input_schema = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 5
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

        response = requests.post(endpoint, json=input_schema)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), output_schema)

    def test_adding_new_comment_with_missing_required_field_post(self):
        import requests
        import json

        endpoint = "https://dummyjson.com/comments/add"
        input_schema = {
            "body": "This makes all sense to me!",
            "userId": 5
        }
        output_schema = None

        response = requests.post(endpoint, json=input_schema)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.json())

    def test_adding_new_comment_with_extra_unexpected_field_post(self):
        import requests
        import json

        endpoint = "https://dummyjson.com/comments/add"
        input_schema = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 5,
            "invalidField": "invalidValue"
        }
        output_schema = None

        response = requests.post(endpoint, json=input_schema)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.json())

    def test_adding_new_comment_with_incorrect_data_type_for_body_or_postid(self):
        import requests
        import json

        endpoint = "https://dummyjson.com/comments/add"
        input_schema = {
            "body": 123,
            "postId": 3,
            "userId": 5
        }
        output_schema = None

        response = requests.post(endpoint, json=input_schema)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.json())

    def test_adding_new_comment_with_invalid_value_for_user_id(self):
        import requests
        import json

        endpoint = "https://dummyjson.com/comments/add"
        input_schema = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": -1
        }
        output_schema = None

        response = requests.post(endpoint, json=input_schema)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.json())

    def test_adding_new_comment_with_boundary_value_for_postid(self):
        import requests
        import json

        endpoint = "https://dummyjson.com/comments/add"
        input_schema = {
            "body": "This makes all sense to me!",
            "postId": 0,
            "userId": 5
        }
        output_schema = None

        response = requests.post(endpoint, json=input_schema)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.json())

    def test_adding_new_comment_with_query_parameter_userid_set_to_0(self):
        import requests
        import json

        endpoint = "https://dummyjson.com/comments/add?userid=0"
        input_schema = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": 0
        }
        output_schema = None

        response = requests.post(endpoint, json=input_schema)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.json())

    def test_adding_new_comment_with_query_parameter_userid_set_to_invalid_value(self):
        import requests
        import json

        endpoint = "https://dummyjson.com/comments/add?userid=invalidValue"
        input_schema = {
            "body": "This makes all sense to me!",
            "postId": 3,
            "userId": "invalidValue"
        }
        output_schema = None

        response = requests.post(endpoint, json=input_schema)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.json())

if __name__ == '__main__':
    unittest.main()