import socket
import json

class ShareDistributor:
    def __init__(self, foreign_servers):
        self.servers = foreign_servers  # List of (IP, PORT)

    def distribute(self, share_dicts):
        """
        share_dicts: List of dicts, one per FS
        Sends share_dicts[i] to servers[i]
        """
        for i, (ip, port) in enumerate(self.servers):
            data = json.dumps(share_dicts[i])
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((ip, port))
                    s.sendall(data.encode())
                    print(f"[+] Sent share to FS {ip}:{port}")
            except Exception as e:
                print(f"[!] Error sending to {ip}:{port} - {e}")
