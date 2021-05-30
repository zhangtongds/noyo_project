import json
import unittest
from server import app, db

SUCCESS_USER_1 = {
    "first_name": "first_1",
    "middle_name": "middle_1",
    "last_name": "last_1",
    "email": "test1@gmail.com",
    "age": "999"
}

SUCCESS_USER_2 = {
    "first_name": "first_2",
    "middle_name": "middle_2",
    "last_name": "last_2",
    "email": "test2@gmail.com",
    "age": "999"
}

FAILED_USER_1 = {
    "first_name": "",
    "middle_name": "middle",
    "last_name": "last",
    "email": "test@gmail.com",
    "age": "999"
}

FAILED_USER_2 = {
    "first_name": "first",
    "middle_name": "middle",
    "last_name": "last",
    "email": "test@gmail.com",
}

FAILED_USER_3 = {
    "user_id": '12345',
    "first_name": "first",
    "middle_name": "middle",
    "last_name": "last",
    "email": "test@gmail.com",
}


class UserTest(unittest.TestCase):
    """This class represents the person API test cases."""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = app.test_client(self)

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_create_user_sucess(self):
        """Test API can create a user success."""
        response = self.client.post("/user", json=SUCCESS_USER_1)
        self.assertEqual(response.status_code, 201)
        self.assertIn("User was successfully created.", str(response.data))

    def test_create_user_fail_empty_first_name_error(self):
        """Test API create a user failed with empty required field."""
        response = self.client.post("/user", json=FAILED_USER_1)
        self.assertEqual(response.status_code, 400)
        self.assertIn("field cannot be empty", str(response.data))

    def test_create_user_missing_required_field_error(self):
        """Test API create a user failed with missing required field """
        response = self.client.post("/user", json=FAILED_USER_2)
        self.assertEqual(response.status_code, 400)
        self.assertIn("key is missing from request body", str(response.data))

    def test_get_user_by_id_default_success(self):
        """Test API can get a user by user_id."""
        create_response = self.client.post("/user", json=SUCCESS_USER_1)
        result = json.loads(create_response.data)
        user_id = result["message"].split()[-1]
        get_response = self.client.get(f"/users/{user_id}")
        self.assertEqual(get_response.status_code, 200)
        self.assertIn(user_id, str(get_response.data))
        self.assertIn("first_1", str(get_response.data))
        self.assertIn("test1@gmail.com", str(get_response.data))
        self.assertEqual(json.loads(get_response.data)["is_latest"], True)

    def test_get_user_not_found_error(self):
        """Test API get a user not found."""
        get_response = self.client.get(f"/users/fake_user_id")
        self.assertEqual(get_response.status_code, 404)
        self.assertIn("not found", str(get_response.data))
    
    def test_update_user_success(self):
        """Test API update user success."""
        create_response = self.client.post("/user", json=SUCCESS_USER_1)
        result = json.loads(create_response.data)
        user_id = result["message"].split()[-1]
        data = {"middle_name": "updated_middle"}
        put_response = self.client.put(f"/users/{user_id}", json=data)
        self.assertEqual(put_response.status_code, 200)
        self.assertIn("updated_middle", str(put_response.data))
        self.assertEqual(json.loads(put_response.data)["is_latest"], True)
        self.assertEqual(json.loads(put_response.data)["version"], 1)
        
        # Test get single user with version number.
        get_response_v0 = self.client.get(f"/users/{user_id}/0")
        self.assertEqual(json.loads(get_response_v0.data)["version"], 0)
        self.assertEqual(json.loads(get_response_v0.data)["is_latest"], False)
        
        get_response_v1 = self.client.get(f"/users/{user_id}/1")
        self.assertEqual(json.loads(get_response_v1.data)["version"], 1)
        self.assertEqual(json.loads(get_response_v1.data)["is_latest"], True)
        
    def test_update_user_forbidden_field_error(self):
        """Test API update user trying to modify user_id field error."""
        create_response = self.client.post("/user", json=SUCCESS_USER_1)
        result = json.loads(create_response.data)
        user_id = result["message"].split()[-1]
        put_response = self.client.put(f"/users/{user_id}", json=FAILED_USER_3)
        self.assertEqual(put_response.status_code, 403)
        self.assertIn("Modifying user_id field is not allowed", str(put_response.data))
    
    def test_delete_single_user_success(self):
        """Test API delete a user success."""
        create_response = self.client.post("/user", json=SUCCESS_USER_1)
        result = json.loads(create_response.data)
        user_id = result["message"].split()[-1]
        delete_response = self.client.delete(f"/users/{user_id}")
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn("deleted", str(delete_response.data))
    
    def test_delete_single_user_not_found_error(self):
        """Test API delete a user success."""
        delete_response = self.client.delete(f"/users/fake_user_id")
        self.assertEqual(delete_response.status_code, 404)
        self.assertIn("not found", str(delete_response.data))     

    def test_get_all_users_success(self):
        """Test API get all users."""
        self.client.post("/user", json=SUCCESS_USER_1)
        self.client.post("/user", json=SUCCESS_USER_2)
        
        get_response = self.client.get(f"/users")
        self.assertEqual(len(json.loads(get_response.data)), 2)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
