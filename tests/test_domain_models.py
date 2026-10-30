
from starlette.testclient import TestClient as TestClient  # noqa
from src.main import app
from datetime import datetime, date
from src.models.models import Complaint, ComplaintStatus, ComplaintStatusEvent, ComplaintCategory, ComplaintPriority
import pytest

client = TestClient(app)


def test_create_customer():
    name = "Maelle"
    last_name = "Reni"
    email = "maelle.reni@example.com"

    response = client.post(
        "/bank/customers",
        json={
            "first_name": name,
            "last_name": last_name,
            "email": email,
            "phone_number": None,
            "segment": None,
            "date_created": datetime.now().isoformat()
        }
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["first_name"] == name
    assert data["last_name"] == last_name
    assert data["email"] == email
    assert data["customer_id"].startswith("CUS")


def test_create_account():
    customer_id = "CUS005"
    account_number = "100000002"
    account_type = "Business"
    status = "ACTIVE"
    current_balance = 50000.00
    response = client.post(
        "/bank/accounts",
        json={
            "customer_id": customer_id,
            "account_number": account_number,
            "account_type": account_type,
            "status": status,
            "opened_date": date.today().isoformat(),
            "current_balance": current_balance
        }
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["customer_id"] == customer_id
    assert data["account_number"] == account_number
    assert data["account_type"] == account_type
    assert data["status"] == status
    assert data["current_balance"] == current_balance
    assert data["account_id"].startswith("ACC")


def test_create_complaint():
    customer_id = "CUS003"
    channel = "Email"
    category = "Online Banking"
    complaint_text = "Login Issue"
    status = "OPEN"
    account_id = "ACC004"
    priority = "Low"

    response = client.post(
        "/bank/complaints",
        json={
            "customer_id": customer_id,
            "channel":channel,
            "category": category,
            "complaint_text":complaint_text,
            "status": status,
            "received_at": datetime.now().isoformat(),
            "account_id": account_id,
            "priority": priority
        }
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["customer_id"] == customer_id
    assert data["complaint_text"] == complaint_text
    assert data["account_id"] == account_id
    assert data["channel"] == channel
    assert data["status"] == status
    assert data["category"] == category
    assert data["priority"] == priority
    assert data["complaint_id"].startswith("CMP")


def test_valid_status_transition():
    complaint = Complaint(
        complaint_id="CMP_TEST",
        status=ComplaintStatus.OPEN
    )

    event = complaint.change_status(
        ComplaintStatus.IN_PROGRESS
    )

    assert complaint.status == ComplaintStatus.IN_PROGRESS
    assert isinstance(event, ComplaintStatusEvent)
    assert event.old_status == ComplaintStatus.OPEN
    assert event.new_status == ComplaintStatus.IN_PROGRESS


def test_invalid_status_transition():
    complaint = Complaint(
        complaint_id="CMP_TEST",
        status=ComplaintStatus.OPEN
    )

    with pytest.raises(ValueError):
        complaint.change_status(ComplaintStatus.CLOSED)

    assert complaint.status == ComplaintStatus.OPEN

def test_closed_complaint_transition():
    complaint = Complaint(
        complaint_id="CMP_TEST",
        status=ComplaintStatus.CLOSED
    )

    with pytest.raises(ValueError):
        complaint.change_status(ComplaintStatus.IN_PROGRESS)

    assert complaint.status == ComplaintStatus.CLOSED

def test_invalid_complaint_category():
    response = client.post(
        "/bank/complaints",
        json={
            "customer_id": "CUS001",
            "account_id": "ACC001",
            "channel": "Phone",
            "category": "Invalid Category",
            "complaint_text": "Incorrect banking fees",
            "status": "OPEN",
            "priority": "High"
        }
    )

    assert response.status_code == 422


def test_invalid_complaint_status():
    response = client.post(
        "/bank/complaints",
        json={
            "customer_id": "CUS001",
            "account_id": "ACC001",
            "channel": "Phone",
            "category": "Fee Dispute",
            "complaint_text": "Unexpected banking fee",
            "status": "PENDING",
            "priority": "High"
        }
    )

    assert response.status_code == 422


def test_invalid_complaint_priority():
    response = client.post(
        "/bank/complaints",
        json={
            "customer_id": "CUS001",
            "account_id": "ACC001",
            "channel": "Phone",
            "category": "Fee Dispute",
            "complaint_text": "Unexpected banking fee",
            "status": "OPEN",
            "priority": "Urgent"
        }
    )

    assert response.status_code == 422



def test_model_invalid_category():
    with pytest.raises(ValueError, match="Invalid category"):
        Complaint(
            complaint_id="CMP_TEST",
            category="Invalid Category"
        )


def test_model_invalid_priority():
    with pytest.raises(ValueError, match="Invalid priority"):
        Complaint(
            complaint_id="CMP_TEST",
            priority="Urgent"
        )


def test_model_invalid_event_status():
    with pytest.raises(ValueError, match="Invalid new_status"):
        ComplaintStatusEvent(
            complaint_id="CMP_TEST",
            new_status="INVALID"
        )
