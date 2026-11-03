from sqlalchemy.orm import Session
from src.models.models import Customer, Complaint, Account, ComplaintStatusEvent, generate_id

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


class ComplaintRepository:
    def create(self,db:Session,complaint_data):
        complaint= Complaint(
            complaint_id=generate_id(db, Complaint),
            customer_id = complaint_data.customer_id,
            channel = complaint_data.channel,
            category= complaint_data.category,
            complaint_text = complaint_data.complaint_text,
            status = complaint_data.status,
            received_at = complaint_data.received_at,
            account_id = complaint_data.account_id,
            priority=complaint_data.priority,
            assigned_analyst_id = complaint_data.assigned_analyst_id
        )

        db.add(complaint)
        db.commit()
        db.refresh(complaint)
        return complaint

    def get_all(self,db:Session):
        return db.query(Complaint).all()


class AccountRepository:
    def create(self,db:Session,account_data):
        account= Account(
            account_id  = generate_id(db, Account),
            customer_id = account_data.customer_id,
            account_number = account_data.account_number,
            account_type= account_data.account_type,
            status = account_data.status,
            opened_date = account_data.opened_date,
            current_balance = account_data.current_balance,
        )

        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    def get_all(self,db:Session):
        return db.query(Account).all()


class ComplaintStatusEventRepository:
    def create(self,db:Session,event_data):
        event= ComplaintStatusEvent(
            complaint_id = event_data.complaint_id,
            new_status = event_data.new_status,
            old_status= event_data.old_status,
            changed_by = event_data.changed_by,
            changed_at = event_data.changed_at,
            comments = event_data.comments,
        )

        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    def get_all(self,db:Session):
        return db.query(ComplaintStatusEvent).all()