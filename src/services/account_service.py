class AccountService:

    def __init__(self, account_repository):
        self.account_repository = account_repository

    def create_account(self, db, account):
        return self.account_repository.create(db, account)

    def get_accounts(self, db):
        return self.account_repository.get_all(db)
    
    def get_accounts_by_customer(self, db, customer_id: str):
        if not isinstance(customer_id, str) or not customer_id.strip():
            raise ValueError("customer_id is required")

        return self.account_repository.get_for_customer(
            db, customer_id
        )