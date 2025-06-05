from user_registry import UserRegistry
from share_generator import ShareGenerator
from share_distributor import ShareDistributor

# Static IPs of Foreign Servers
FOREIGN_SERVERS = [
    ("192.168.0.2", 8001),
    ("192.168.0.3", 8002),
    ("192.168.0.4", 8003),
]

N_SHARES = 3
THRESHOLD = 2

def main():
    registry = UserRegistry()
    generator = ShareGenerator(N_SHARES,THRESHOLD)
    distributor = ShareDistributor(FOREIGN_SERVERS)

    # Step 1: Register 3 users
    for _ in range(3):
        user_id = input("Enter user name: ").strip()
        key = input("Enter secret key: ").strip()
        registry.add_user(user_id, key)

    # Step 2: Generate shares
    user_dict = registry.get_all_users()
    registry.save_users_to_file(user_dict)  # Save to file

    user_dict = registry.load_users_from_file()
    shares = generator.create_shares(user_dict)
    print("\nGenerated Shares:")

    for idx, share_set in enumerate(shares):
        print(f"Foreign Server {idx+1} gets: {share_set}")

    # Step 3: Distribute shares
    distributor.distribute(shares)

if __name__ == "__main__":
    main()
