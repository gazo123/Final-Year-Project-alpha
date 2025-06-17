import random

class ShareGenerator:
     def __init__(self, n, t):
          self.n = n
          self.t = t
          self.prime=2089

     def eval_polynomial(self, coeffs, x):
          result = 0
          for power, coef in enumerate(coeffs):
               result += coef * (x ** power)
          return result % self.prime

     def create_shares(self, user_dict):
          all_shares = [{} for _ in range(self.n)]  # List of n dicts, one for each FS

          for user, secret in user_dict.items():
               secret_int = secret

               # Generate polynomial coefficients
               coeffs = [secret_int] + [random.randint(0, self.prime - 1) for _ in range(self.t - 1)]

               # Generate n (x, y) shares
               for i in range(1, self.n + 1):
                    x = i
                    y = self.eval_polynomial(coeffs, x)
                    all_shares[i - 1][user] = (x, y)  # Store as tuple

          return all_shares

