from src.repositories.complaint_status_event_repository_sqlalchemy import ComplaintStatusEventRepository
from src.repositories.complaint_repository_sqlalchemy import ComplaintRepository


class ComplaintService:
    def __init__(self, complaint_repository, customer_repository, account_repository):
        self.complaint_repository = complaint_repository
        self.customer_repository = customer_repository
        self.account_repository = account_repository
    
    def create_complaint(self,db, complaint):
        # Verify that the customer exists
        customer = self.customer_repository.get_by_id(db, complaint.customer_id)
        if customer is None:
            raise ValueError(f"Customer {complaint.customer_id} does not exist")

        #Verify that the account exists
        if complaint.account_id is not None:
            account = self.account_repository.get_by_id(db, complaint.account_id)
            if account is None:
                raise ValueError(f"Account {complaint.account_id} does not exist")

            #Verify it is one of the customer's
            if account.customer_id!=complaint.customer_id:
                raise ValueError(f"Account {complaint.account_id} does not belong to customer {complaint.customer_id}")
        return self.complaint_repository.create(db,complaint)

    def get_complaints(self,db):
        return self.complaint_repository.get_all(db)

    def get_complaint_by_id(self, db, complaint_id):
        complaint = self.complaint_repository.get_by_id(db, complaint_id)
        if complaint is None:
            raise ValueError(f"Complaint {complaint_id} does not exist")
        return complaint

    def change_status(self, db, complaint_id, new_status, changed_by=None, comments=None):
        complaint=self.get_complaint_by_id(db, complaint_id)
        event= complaint.change_status(
            new_status = new_status,
            changed_by = changed_by,
            comments = comments)
        return self.complaint_repository.save_status_change(db, complaint, event)

    def get_customer_complaints(self, db, customer_id):
        customer = self.customer_repository.get_by_id(db, customer_id)

        if customer is None:
            raise ValueError(f"Customer {customer_id} does not exist")

        return self.complaint_repository.get_by_customer_id(db,customer_id)

    def get_complaint_with_history(self, db, complaint_id: str):

        complaint = self.complaint_repository.get_by_id(db, complaint_id)

        if complaint is None:
            return None

        history = ComplaintStatusEventRepository().get_by_complaint_id(db, complaint_id)

        return {
            "complaint_id": complaint.complaint_id,
            "customer_id": complaint.customer_id,
            "account_id": complaint.account_id,
            "category": complaint.category.value,
            "status": complaint.status.value,
            "priority": (
                complaint.priority.value
                if complaint.priority is not None
                else None
            ),
            "received_at": (
                complaint.received_at.isoformat()
                if complaint.received_at is not None
                else None
            ),
            "status_history": [
                {
                    "history_id": event.history_id,
                    "old_status": (
                        event.old_status.value
                        if event.old_status is not None
                        else None
                    ),
                    "new_status": event.new_status.value,
                    "changed_by": event.changed_by,
                    "changed_at": (
                        event.changed_at.isoformat()
                        if event.changed_at is not None
                        else None
                    ),
                    "comments": event.comments,
                }
                for event in history
            ],
        }