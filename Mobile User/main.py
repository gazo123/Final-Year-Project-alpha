from config import FOREIGN_SERVERS
from mobile_user import MobileUser
   
def main():
    print("=== Mobile User Menu ===")

    username = input("Enter your username: ").strip()
    key = input("Enter your secret key: ").strip()

    pid = MobileUser.compute_pid(username, key)   #hashing the username and 
    print(f"[→] Computed PID: {pid}")

    print("\nSelect Foreign Server to send to:")
    for idx, (ip, port) in FOREIGN_SERVERS.items():
        print(f"  {idx}. {ip}:{port}")

    choice = input("Enter option (1/2/3): ").strip()
    if choice not in FOREIGN_SERVERS:
        print("[!] Invalid choice. Exiting.")
        return

    target_ip, target_port = FOREIGN_SERVERS[choice]
    MobileUser.send_pid_to_foreign_server(username, pid, target_ip, target_port)

if __name__ == "__main__":
    main()
