from user_registry import UserRegistry
from share_generator import ShareGenerator
from share_distributor import ShareDistributor
from config import FOREIGN_SERVERS, N_SHARES, THRESHOLD, SHARE_FILE_NAME


if __name__ == "__main__":
    registry = UserRegistry(SHARE_FILE_NAME)
    generator = ShareGenerator(N_SHARES,THRESHOLD)
    distributor = ShareDistributor(FOREIGN_SERVERS)

    # Step 1: Register users
    num_users = 2
    for _ in range(num_users):
        user_id = input("Enter user name: ").strip()
        key = int(input("Enter secret key: ").strip())
        registry.add_user(user_id, key)
    
    user_dict = registry.get_all_users()
    registry.save_users_to_file(user_dict)          # Save shares to file

    # Step 2: Generate shares
    user_dict = registry.load_users_from_file()
    shares = generator.create_shares(user_dict)     #creating shares

    # Step 3: Distribute shares
    distributor.distribute(shares)
