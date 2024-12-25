import unittest

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.valid_users = [
            {"username": "Stamate Constantin", "email": "constantinstamate.r@gmail.com", "password": "1234"},
            {"username": "Ion Popescu", "email": "ion.popescu@example.com", "password": "abcd"},
            {"username": "Maria Ionescu", "email": "maria.ionescu@example.com", "password": "5678"},
            {"username": "Andrei Georgescu", "email": "andrei.georgescu@example.com", "password": "qwerty"},
            {"username": "Elena Vasile", "email": "elena.vasile@example.com", "password": "pass1234"},
            {"username": "Victor Mihail", "email": "victor.mihail@example.com", "password": "password123"}
        ]

    def test_login_success(self):
        email_input = "constantinstamate.r@gmail.com"
        password_input = "1234"

        user_exists = any(user['email'] == email_input for user in self.valid_users)

        self.assertTrue(user_exists, f"Expected user with email {email_input} to exist, but it was not found.")

    def test_login_failure(self):
        email_input = "mariapopescu.r@gmail.com"
        password_input = "mar121321ia"

        user_exists = any(user['email'] == email_input for user in self.valid_users)

        self.assertFalse(user_exists, f"Expected user with email {email_input} to not exist, but it was found.")

if __name__ == "__main__":
    unittest.main()
