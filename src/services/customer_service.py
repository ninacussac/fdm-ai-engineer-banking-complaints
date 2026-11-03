class CustomerService:
    def __init__(self, customer_repository):
        self.repository = customer_repository

    def create_customer(self,db, customer):
        return self.repository.create(db,customer)

    def get_customers(self,db):
        return self.repository.get_all(db)