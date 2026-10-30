class AccountService:

    def __init__(self, account_repository):
        self.account_repository = account_repository

    def create_account(self, db, account):
        return self.account_repository.create(db, account)

    def get_accounts(self, db):
        return self.account_repository.get_all(db)