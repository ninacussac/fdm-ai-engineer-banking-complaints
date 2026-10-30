from src.repositories import DatabaseManager
from src.repositories.account_repository import AccountRepository

def main():
    db = DatabaseManager()
    account_repo = AccountRepository(db)

    # test existing customer 
    accounts = account_repo.get_for_customer("C0100")

    if accounts :
        print(f"Found {len(accounts)} account(s):")
        for account in accounts:
            print(account)
    else:
        print("No Account found for this customer.")

    # test non existing customer
    accounts = account_repo.get_for_customer("C9999")

    if accounts :
        print(f"Found {len(accounts)} account(s):")
        for account in accounts:
            print(account)
    else:
        print("No Account found for this customer.")


if __name__ == "__main__":
    main()