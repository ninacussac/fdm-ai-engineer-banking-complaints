from sqlalchemy.orm import Session
from src.models.models import Customer, generate_id

class CustomerRepository:
    def create(self,db:Session,customer_data):
        customer= Customer(
            customer_id = generate_id(db, Customer),
            first_name = customer_data.first_name,
            last_name = customer_data.last_name,
            email= customer_data.email,
            phone_number = customer_data.phone_number,
            segment = customer_data.segment,
            date_created = customer_data.date_created
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    def get_all(self,db:Session):
        return db.query(Customer).all()

    def get_by_id(self, db: Session, customer_id: str):
        return db.get(Customer, customer_id)
