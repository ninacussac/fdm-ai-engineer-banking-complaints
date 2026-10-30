from src.repositories.customer_repository_sqlalchemy import CustomerRepository, ComplaintStatusEventRepository, ComplaintRepository, AccountRepository

class CustomerService:
    def __init__(self):
        self.repository = CustomerRepository()

    def create_customer(self,db, customer):
        return self.repository.create(db,customer)

    def get_customers(self,db):
        return self.repository.get_all(db)


class ComplaintService:
    def __init__(self):
        self.repository = ComplaintRepository()

    def create_complaint(self,db, complaint):
        return self.repository.create(db,complaint)

    def get_complaints(self,db):
        return self.repository.get_all(db)


class AccountService:
    def __init__(self):
        self.repository = AccountRepository()

    def create_account(self,db, account):
        return self.repository.create(db,account)

    def get_accounts(self,db):
        return self.repository.get_all(db)


class ComplaintStatusEventService:
    def __init__(self):
        self.repository = ComplaintStatusEventRepository()

    def create_event(self,db, event):
        return self.repository.create(db,event)

    def get_events(self,db):
        return self.repository.get_all(db)
