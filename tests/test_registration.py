import unittest

class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.valid_users = [
            {"username": "Stamate Constantin", "email": "constantinstamate.r@gmail.com", "password": "1234"},
            {"username": "Ion Popescu", "email": "ion.popescu@example.com", "password": "abcd"},
            {"username": "Maria Ionescu", "email": "maria.ionescu@example.com", "password": "5678"},
            {"username": "Andrei Georgescu", "email": "andrei.georgescu@example.com", "password": "qwerty"},
            {"username": "Elena Vasile", "email": "elena.vasile@example.com", "password": "pass1234"},
            {"username": "Victor Mihail", "email": "victor.mihail@example.com", "password": "password123"}
        ]

    def test_registration(self):
        new_user = {"username": "George Enescu", "email": "george.enescu@example.com", "password": "george123"}

        user_exists = any(user['email'] == new_user['email'] for user in self.valid_users)

        if not user_exists:
            self.valid_users.append(new_user)
            print(f"User {new_user['email']} successfully added.")
            user_exists = True 

        self.assertTrue(user_exists, f"Expected user with email {new_user['email']} to be added, but it was not.")

if __name__ == "__main__":
    unittest.main()
