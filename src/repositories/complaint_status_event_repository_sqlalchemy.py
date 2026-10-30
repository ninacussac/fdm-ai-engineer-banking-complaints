
from sqlalchemy.orm import Session

from src.models.models import ComplaintStatusEvent


class ComplaintStatusEventRepository:

    def create(self, db: Session, event_data):
        event = ComplaintStatusEvent(
            complaint_id=event_data.complaint_id,
            new_status=event_data.new_status,
            old_status=event_data.old_status,
            changed_by=event_data.changed_by,
            changed_at=event_data.changed_at,
            comments=event_data.comments,
        )

        db.add(event)
        db.commit()
        db.refresh(event)

        return event

    def get_all(self, db: Session):
        return db.query(ComplaintStatusEvent).all()
