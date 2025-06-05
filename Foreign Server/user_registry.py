import json

class UserRegistry:
     def __init__(self):
          self.filename = "received_shares.json"

     def save_shares(self,shares):
          with open(self.filename, "w") as f:
               json.dump(shares, f, indent=4)
          print(f"[$] Shares saved to {self.filename}")

     
     def load_shares(self):
          try:
               with open(self.filename, "r") as f:
                    return json.load(f)
          except FileNotFoundError:
               return {}