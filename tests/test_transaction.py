from uuid import uuid4
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import event

from src.main import app
from src.data.connection import SessionLocal
from src.models.models import ComplaintStatusEvent, Complaint, ComplaintCategory, ComplaintStatus, ComplaintPriority


client = TestClient(app)

def test_create_complaint_with_initial_event():
    unique_text = f"Transaction test {uuid4().hex}"

    response = client.post(
        "/complaints",
        json={
            "customer_id": "CUS001",
            "account_id": "ACC001",
            "channel": "Online",
            "category": "Fee Dispute",
            "complaint_text": unique_text,
            "status": "OPEN",
            "priority": "Medium"
        }
    )

    assert response.status_code == 201

    complaint_id = response.json()["complaint_id"]

    with SessionLocal() as db:
        events = (db.query(ComplaintStatusEvent).filter_by(complaint_id=complaint_id).all())

        assert len(events) == 1
        assert events[0].old_status is None
        assert events[0].new_status.value == "OPEN"


def test_rollback():
    with SessionLocal() as db:
        complaint = Complaint(
            complaint_id="CMP_ROLLBACK_TEST",
            customer_id="CUS001",
            channel="Online",
            category=ComplaintCategory.FEE_DISPUTE,
            complaint_text="Rollback test",
            status=ComplaintStatus.OPEN,
            priority=ComplaintPriority.MEDIUM
        )

        db.add(complaint)
        db.flush()

        # Simulate a failure before commit
        db.rollback()

    with SessionLocal() as db:
        saved_complaint = db.get(Complaint, "CMP_ROLLBACK_TEST")
        assert saved_complaint is None




def test_rollback_when_event_fails():
    with SessionLocal() as db:
        initial_count = db.query(Complaint).count()

    # declenche une exception volontairement
    def fail_event_insert(mapper, connection, target):
        raise RuntimeError("Simulated event failure")

    # dire a sqlalchemy quand declencher l'erreur
    event.listen(ComplaintStatusEvent, "before_insert", fail_event_insert)

    try:
        response = client.post("/complaints",
                    json={
                    "customer_id": "CUS001",
                    "account_id": "ACC001",
                    "channel": "Online",
                    "category": "Fee Dispute",
                    "complaint_text": "Rollback API test",
                    "status": "OPEN",
                    "priority": "Medium"
                }
            )
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal server error"
    finally:
        event.remove(ComplaintStatusEvent, "before_insert", fail_event_insert)

    with SessionLocal() as db:
        final_count = db.query(Complaint).count()

    assert final_count == initial_count