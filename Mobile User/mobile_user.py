import socket
import json
import hashlib

# List of Foreign Servers (IP, PORT)
FOREIGN_SERVERS = {
    "1": ("192.168.0.111", 9002),
    "2": ("192.168.0.3", 9102),
    "3": ("192.168.0.4", 9202),
}

def compute_pid(username, key):
    pid_input = f"{username}:{key}"
    return hashlib.sha256(pid_input.encode()).hexdigest()

def send_pid_to_foreign_server(username, pid, target_ip, target_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_ip, target_port))
            payload = json.dumps({username: pid})
            s.sendall(username.encode())  # or s.sendall(payload.encode()) if FS expects JSON
            print(f"[✓] Sent PID for '{username}' to {target_ip}:{target_port}")
    except Exception as e:
        print(f"[!] Error sending to FS: {e}")

def main():
    print("=== Mobile User Menu ===")

    username = input("Enter your username: ").strip()
    key = input("Enter your secret key: ").strip()

    pid = compute_pid(username, key)   #hashing the username and 
    print(f"[→] Computed PID: {pid}")

    print("\nSelect Foreign Server to send to:")
    for idx, (ip, port) in FOREIGN_SERVERS.items():
        print(f"  {idx}. {ip}:{port}")

    choice = input("Enter option (1/2/3): ").strip()
    if choice not in FOREIGN_SERVERS:
        print("[!] Invalid choice. Exiting.")
        return

    target_ip, target_port = FOREIGN_SERVERS[choice]
    send_pid_to_foreign_server(username, pid, target_ip, target_port)

if __name__ == "__main__":
    main()
