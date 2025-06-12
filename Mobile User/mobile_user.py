import socket
import json
import hashlib
from config import MOBILE_USER_IP,MOBILE_AUTHENTICATION_PORT
class MobileUser:
    #------------------------------------------------------------------------------------------------------------------------------------------
    def compute_pid(username, key):
        pid_input = f"{username}:{key}"
        return hashlib.sha256(pid_input.encode()).hexdigest()

    #----------------------------------------------------------------------------------------------------------------------------------------------
    def send_pid_to_foreign_server(username, pid, target_ip, target_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((target_ip, target_port))
                payload = json.dumps({username: pid})
                s.sendall(payload.encode()) # s.sendall(username.encode()) 
                print(f"[✓] Sent PID for '{username}' to {target_ip} : {target_port}")
        except Exception as e:
            print(f"[!] Error sending to FS: {e}")
    #----------------------------------------------------------------------------------------------------------------------------------------------
    def authentication_message_listener():
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.bind((MOBILE_USER_IP,MOBILE_AUTHENTICATION_PORT))
            s.listen()

            print("[*] Listening for authentication messages...")
            while True:
                conn, addr = s.accept()
                with conn:
                    msg = conn.recv(1024).decode()
                    print(msg)