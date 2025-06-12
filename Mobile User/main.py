from config import FOREIGN_SERVERS
from mobile_user import MobileUser
import threading
   
if __name__ == "__main__":
    print("=== Mobile User Menu ===")

    username = input("Enter your username: ").strip()
    key = input("Enter your secret key: ").strip()
    print(f"Key: {key}")                            #DEBUG CODE
    pid = MobileUser.compute_pid(username, key)   #hashing the username and 
    print(f"[→] Computed PID: {pid}")               #DEBUG CODE


    print("\nSelect Foreign Server to send to:")
    for idx, (ip, port) in FOREIGN_SERVERS.items():
        print(f"Foreign Server {idx}:  {ip}:{port}")
    
    choice = input("Enter option (1/2/3): ").strip()

    #switching on the authentication message reply listener
    threading.Thread(target=MobileUser.authentication_message_listener(),daemon=True).start()

    if choice in FOREIGN_SERVERS:
        target_ip, target_port = FOREIGN_SERVERS[choice]
        MobileUser.send_pid_to_foreign_server(username, pid, target_ip, target_port)
    else:
        print("[!] Invalid choice. Exiting.")

