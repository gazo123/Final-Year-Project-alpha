from foreign_server import ForeignServer
import threading
from user_registry import UserRegistry
from config import RECEIVE_SHARE_FILE_PATH

if __name__ == "__main__":
    
    # Step 1: Run the initial share receiver
    ForeignServer.start_foreign_server()

    print("\n[✓] Received initial shares. Starting listeners...\n")

    # Step 2: Start background listeners
    threading.Thread(target=ForeignServer.get_share_request_listener, daemon=True).start()
    threading.Thread(target=ForeignServer.mobile_user_request_listener, daemon=True).start()

    # Step 3: Interactive main thread menu
    while True:
        print("\n------ Foreign Server Menu ------")
        print("1. Display all stored shares")
        print("2. Exit")
        choice = input("Select an option (1/2): ").strip()

        if choice == "1":
            registry= UserRegistry(RECEIVE_SHARE_FILE_PATH)
            shares = registry.load_shares()
            if shares:
                print("\n[$] Stored Shares:")
                for user, share in shares.items():
                    print(f"  - {user}: {share}")
            else:
                print("[!] No shares stored yet.")

        elif choice == "2":
            print("Exiting...")
            break

        else:
            print("[!] Invalid option. Try again.")
