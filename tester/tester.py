import random
import hashlib

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
            # a known Mersenne prime (very large)

          for user, secret in user_dict.items():
               # Convert secret string to integer
               # secret_bytes = secret.encode('utf-8')
               # secret_int = int.from_bytes(secret_bytes, byteorder='big') % prime
               secret_int = secret

               # Generate polynomial coefficients
               coeffs = [secret_int] + [random.randint(0, self.prime - 1) for _ in range(self.t - 1)]

               # Generate n (x, y) shares
               for i in range(1, self.n + 1):
                    x = i
                    y = self.eval_polynomial(coeffs, x)
                    all_shares[i - 1][user] = (x, y)  # Store as tuple

          return all_shares

def reconstruct_key(shares):
    """
    Reconstructs the original secret using Lagrange interpolation.
    shares: list of (x, y) tuples
    prime: the same prime used for share generation
    """
    prime = 2089  # a known Mersenne prime (very large)

    def _lagrange_basis(j, x_values):
        num, den = 1, 1
        xj = x_values[j]
        for m, xm in enumerate(x_values):
            if m != j:
                num = (num * -xm) % prime
                den = (den * (xj - xm)) % prime
        return (num * pow(den, -1, prime)) % prime  # mod inverse

    x_values = [x for x, _ in shares]
    y_values = [y for _, y in shares]

    secret = 0
    for j in range(len(shares)):
        lj = _lagrange_basis(j, x_values)
        secret = (secret + y_values[j] * lj) % prime

    return secret

def compute_pid(username, key):
    pid_input = f"{username}:{key}"
    return hashlib.sha256(pid_input.encode()).hexdigest()

if __name__ == "__main__":
     generator = ShareGenerator(3,2)

     #creating shares
     user_dict = {'user1':111,'user2':222,'user3':333}
     username = input("enter the username: ")
     print(f"original key for user {user_dict[username]}")

     pid1 = compute_pid(username, user_dict[username])

     all_shares = generator.create_shares(user_dict)
     # print(f"created shares: {all_shares}")

     #reconstructing key
     shares=[share[username] for share in all_shares]
     secret = reconstruct_key(shares)
     print(f"reconstructed key {secret}")

     pid2 =  compute_pid(username, secret)

     if pid1 == pid2:
          print("authentication successful")
     else:
          print("Authentication unsuccessful")