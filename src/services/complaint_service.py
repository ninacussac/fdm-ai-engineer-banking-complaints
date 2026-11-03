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
            comments = comments
        )
        return self.complaint_repository.save_status_change(db, complaint, event)