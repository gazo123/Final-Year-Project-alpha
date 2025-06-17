import socket
from config import HOST,PORT,GET_SHARE_PORT,MOBILE_USER_PORT,RECEIVE_SHARE_FILE_PATH,MOBILE_AUTHENTICATION_PORT
from user_registry import UserRegistry
import json
import ast
import hashlib

registry = UserRegistry(RECEIVE_SHARE_FILE_PATH)

class ForeignServer:
     def __init__(self):
          pass

     def start_foreign_server():
          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
               s.bind((HOST, PORT))
               s.listen(5)
               print(f"[+] Foreign Server listening on {HOST}:{PORT}")

               while True:
                    conn, addr = s.accept()
                    with conn:
                         print(f"[+] Connected by {addr}")
                         data = conn.recv(4096).decode()
                         if data:
                              try:
                                   shares = json.loads(data)
                                   print(f"[✓] Received shares: {shares}")
                                   registry.save_shares(shares)
                                   break
                              except json.JSONDecodeError:
                                   print("[!] Received invalid JSON.")

     #-----------------------------------------------------------------------------------------------------------------------------------

     def get_share_request_listener():
          """Returns user's share when requested by another FS (via Home Server relay)"""

          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
               s.bind((HOST, GET_SHARE_PORT))
               s.listen()
               print(f"[$] Listening for share requests on port {GET_SHARE_PORT}...")

               while True:
                    conn, addr = s.accept()
                    with conn:
                         username = conn.recv(1024).decode().strip()
                         print(f"[→] Share requested for '{username}' from {addr}")
                         shares = registry.load_shares()
                         share = shares.get(username, "NOT_FOUND")
                         conn.sendall(json.dumps(share).encode())
                         print(f"[✓] Sent share: {share}")

     #--------------------------------------------------------------------------------------------------------------------------------------
     def send_share_request(username):
          other_servers = [("192.168.0.2", GET_SHARE_PORT),("192.168.0.4", GET_SHARE_PORT)]  # Replace with actual FS IPs & exclude own
          print(f"[→] Requesting shares for '{username}'...")
          responses=[]

          for ip, port in other_servers:
               try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                         s.connect((ip, port))
                         s.sendall(username.encode())
                         response = s.recv(4096).decode()
                         print(f"[✓] Share from {ip}:{port} → {response}")
                         responses.append(response)
               except Exception as e:
                    print(f"[!] Failed to get share from {ip}:{port} - {e}")
          return responses
     
     #-------------------------------------------------------------------------------------------------------------------------------------
     def mobile_user_request_listener():
          
          def send_authentication_message(mobile_ip, mobile_port, msg):
               with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                    s.connect((mobile_ip,mobile_port))
                    s.sendall(msg.encode())
                    
          # ------------------------------------------------------------------------------------------

          def reconstruct_key(shares):
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
          #------------------------------------------------------------------------------------------------------------------
          def authenticate_mu():
               #-----------------------------------------------------------
               def _compute_pid(username, key):
                    pid_input = f"{username}:{key}"
                    return hashlib.sha256(pid_input.encode()).hexdigest()
               #-----------------------------------------------------------
               shares = registry.load_shares()
               if username in shares:
                    print(f"[+] Sent result found")

                    rest_shares =ForeignServer.send_share_request(username)          #getting all shares into rest_shares
                    rest_shares = [tuple(ast.literal_eval(i)) for i in rest_shares]
                    own_share = shares.get(username)
                    rest_shares.append(tuple(own_share))
                    
                    reconstructed_key = reconstruct_key(rest_shares)
                    new_pid = _compute_pid(username,reconstructed_key)

                    if pid == new_pid:
                         print(f"[+] USER AUTHENTICATION SUCCESSFUL") #DEBUG
                         send_authentication_message(mobile_ip, MOBILE_AUTHENTICATION_PORT, "[+] USER AUTHENTICATION SUCCESSFUL")

                    else:
                         print("[!] USER AUTHENTICATION UNSUCCESSFUL") #DEBUG
                         send_authentication_message(mobile_ip, MOBILE_AUTHENTICATION_PORT, "[!] USER AUTHENTICATION UNSUCCESSFUL")

               else:
                    print("[!] USERNAME NOT FOUND")

          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
               s.bind((HOST, MOBILE_USER_PORT))
               s.listen()
               print(f"[$] Listening for Mobile User requests on port {MOBILE_USER_PORT}...")
               while True:
                    conn, addr = s.accept()
                    mobile_ip,_=addr
                    with conn:
                         payload = conn.recv(1024).decode().strip()
                         payload = ast.literal_eval(payload)
                         username, pid = next(iter(payload.items()))

                         print(f"[-] Mobile user lookup for '{username}' from {addr}")
                         authenticate_mu(username, pid, payload)
                         return #possible error
