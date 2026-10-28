from datetime import datetime
import pytest

from src.domain.models import (
    Complaint,
    ComplaintCategory,
    ComplaintPriority,
    ComplaintStatus,
    ComplaintStatusEvent
)


def test_create_valid_complaint():
    complaint = Complaint(
        complaint_id="CMP001",
        customer_id="C001",
        channel="Online",
        category=ComplaintCategory.FRAUD_CLAIM,
        complaint_text="Suspicious transaction",
        status=ComplaintStatus.OPEN,
        received_at=datetime.now()
    )

    assert complaint.complaint_id == "CMP001"
    assert complaint.status == ComplaintStatus.OPEN
    assert complaint.category == ComplaintCategory.FRAUD_CLAIM

def test_invalid_complaint_category():
    with pytest.raises(ValueError, match="Invalid complaint category"):
        Complaint(
            complaint_id="CMP002",
            customer_id="C001",
            channel="Online",
            category="INVALID_CATEGORY",
            complaint_text="Incorrect fee charged",
            status=ComplaintStatus.OPEN,
            received_at=datetime.now()
        )

def test_invalid_complaint_status():
    with pytest.raises(ValueError, match="Invalid complaint status"):
        Complaint(
            complaint_id="CMP003",
            customer_id="C001",
            channel="Online",
            category=ComplaintCategory.FRAUD_CLAIM,
            complaint_text="Suspicious transaction",
            status="INVALID_STATUS",
            received_at=datetime.now()
        )

def test_invalid_complaint_priority():
    with pytest.raises(ValueError, match="Invalid complaint priority"):
        Complaint(
            complaint_id="CMP004",
            customer_id="C001",
            channel="Online",
            category=ComplaintCategory.FRAUD_CLAIM,
            complaint_text="Incorrect banking fees",
            status=ComplaintStatus.OPEN,
            received_at=datetime.now(),
            priority="VERY_URGENT"
        )

def test_valid_status_transition():
    complaint = Complaint(
        complaint_id="CMP005",
        customer_id="C001",
        channel="Online",
        category=ComplaintCategory.FRAUD_CLAIM,
        complaint_text="Suspicious transaction",
        status=ComplaintStatus.OPEN,
        received_at=datetime.now()
    )

    event = complaint.change_status(
        new_status=ComplaintStatus.IN_PROGRESS,
        changed_by="EMP001"
    )

    assert complaint.status == ComplaintStatus.IN_PROGRESS
    assert event.old_status == ComplaintStatus.OPEN
    assert event.new_status == ComplaintStatus.IN_PROGRESS
    assert event.complaint_id == "CMP005"
    assert event.changed_by == "EMP001"


def test_invalid_status_transition():
    complaint = Complaint(
        complaint_id="CMP006",
        customer_id="C001",
        channel="Online",
        category=ComplaintCategory.FRAUD_CLAIM,
        complaint_text="Suspicious transaction",
        status=ComplaintStatus.OPEN,
        received_at=datetime.now()
    )

    with pytest.raises(ValueError, match="Invalid transition"):
        complaint.change_status(
            new_status=ComplaintStatus.CLOSED
        )

    assert complaint.status == ComplaintStatus.OPEN

def test_valid_status_event():
    event = ComplaintStatusEvent(
        complaint_id="CMP001",
        old_status=ComplaintStatus.OPEN,
        new_status=ComplaintStatus.IN_PROGRESS,
        changed_by="EMP001",
        comments="Complaint assigned to an analyst"
    )

    assert event.complaint_id == "CMP001"
    assert event.old_status == ComplaintStatus.OPEN
    assert event.new_status == ComplaintStatus.IN_PROGRESS
    assert event.changed_by == "EMP001"
    assert event.history_id is None
    assert isinstance(event.changed_at, datetime)

def test_invalid_status_event():
    with pytest.raises(ValueError, match="Invalid new status"):
        ComplaintStatusEvent(
            complaint_id="CMP001",
            new_status="INVALID_STATUS"
        )