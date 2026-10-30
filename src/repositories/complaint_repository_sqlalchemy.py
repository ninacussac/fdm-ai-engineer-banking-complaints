
from sqlalchemy.orm import Session

from src.models.models import (
    Complaint,
    ComplaintStatusEvent,
    generate_id,
)


class ComplaintRepository:

    def create(self, db: Session, complaint_data):
        complaint = Complaint(
            complaint_id=generate_id(db, Complaint),
            customer_id=complaint_data.customer_id,
            channel=complaint_data.channel,
            category=complaint_data.category,
            complaint_text=complaint_data.complaint_text,
            status=complaint_data.status,
            received_at=complaint_data.received_at,
            account_id=complaint_data.account_id,
            priority=complaint_data.priority,
            assigned_analyst_id=complaint_data.assigned_analyst_id,
        )

        db.add(complaint)
        db.commit()
        db.refresh(complaint)

        return complaint

    def get_all(self, db: Session):
        return db.query(Complaint).all()

    def get_by_id(self, db: Session, complaint_id: str):
        return db.get(Complaint, complaint_id)

    def save_status_change(
        self,
        db: Session,
        complaint: Complaint,
        event: ComplaintStatusEvent,
    ):
        try:
            db.add(complaint)
            db.add(event)

            db.commit()

            db.refresh(complaint)
            db.refresh(event)

            return complaint, event

        except Exception:
            db.rollback()
            db.expire_all()
            raise
