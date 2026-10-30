class CustomerService:
    def __init__(self, customer_repository):
        self.repository = customer_repository

    def create_customer(self,db, customer):
        return self.repository.create(db,customer)

    def get_customers(self,db):
        return self.repository.get_all(db)

    def get_customer_by_id(self,db,customer_id):
        customer = self.repository.get_by_id(db,customer_id)

        if customer is None:
            raise ValueError(f"Customer {customer_id} does not exist")
        return customer