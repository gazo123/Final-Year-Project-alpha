import socket
import json
from user_registry import UserRegistry
import threading

HOST = '192.168.0.3'  # Change this to match this server's static IP
PORT = 8001           # Change to the correct port for this FS
GET_SHARE_PORT = 9001
MOBILE_USER_PORT = 9002

registry = UserRegistry()

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
#----------------------------------------------------------------------------------------------------------------------------------
def send_share_request(username):
    other_servers = [("192.168.0.2", GET_SHARE_PORT), ("192.168.0.4", GET_SHARE_PORT)]  # Replace with actual FS IPs & exclude own
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

#-------------------------------------------------------------------------------------------------------------------------------------
def mobile_user_request_listener():
    """Checks if Mobile User's username exists in own shares"""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, MOBILE_USER_PORT))
        s.listen()
        print(f"[$] Listening for Mobile User requests on port {MOBILE_USER_PORT}...")
        while True:
            conn, addr = s.accept()
            with conn:
                username = conn.recv(1024).decode().strip()
                print(f"[👤] Mobile user lookup for '{username}' from {addr}")
                shares = registry.load_shares()
                result = "FOUND" if username in shares else "NOT_FOUND"
                conn.sendall(result.encode())
                print(f"[✓] Sent result: {result}")


#----------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # Step 1: Run the initial share receiver
    start_foreign_server()

    print("\n[✓] Received initial shares. Starting listeners...\n")

    # Step 2: Start background listeners
    threading.Thread(target=get_share_request_listener, daemon=True).start()
    threading.Thread(target=mobile_user_request_listener, daemon=True).start()

    # Step 3: Interactive main thread menu
    while True:
        print("\n------ Foreign Server Menu ------")
        print("1. Send share request for username")
        print("2. Display all stored shares")
        print("3. Exit")
        choice = input("Select an option (1/2/3): ").strip()

        if choice == "1":
            username = input("Enter username to request shares: ").strip()
            shares =send_share_request(username)
            for share in shares:
                print(share)

        elif choice == "2":
            shares = registry.load_shares()
            if shares:
                print("\n[$] Stored Shares:")
                for user, share in shares.items():
                    print(f"  - {user}: {share}")
            else:
                print("[!] No shares stored yet.")

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("[!] Invalid option. Try again.")
