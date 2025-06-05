import json
import os
class UserRegistry:
    def __init__(self):
        self.users = {}  # {user_id: secret_key}
        self.filename="user_data/registered_users.json"

    def add_user(self, user_id, key):
        self.users[user_id] = key

    def get_all_users(self):
        return self.users

    def save_users_to_file(self,user_dict):
        with open(self.filename, 'w') as f:
            json.dump(user_dict, f, indent=4)
        print(f"\nRegistered users saved to {self.filename}")

    def load_users_from_file(self):
        if not os.path.exists(self.filename):
            print("No existing user data found.")
            return {}
        with open(self.filename, 'r') as f:
            user_dict = json.load(f)
        print(f"Loaded users from {self.filename}")
        return user_dict
