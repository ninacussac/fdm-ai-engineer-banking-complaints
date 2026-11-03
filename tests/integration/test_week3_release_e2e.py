
from src.models.models import Complaint, ComplaintStatusEvent


def test_week3_release_end_to_end(client, test_db):
    # Step 1: Create a complaint
    response = client.post(
        "/complaints",
        json={
            "customer_id": "CUS001",
            "account_id": "ACC001",
            "channel": "Online",
            "category": "Fee Dispute",
            "complaint_text": "Incorrect fee charged",
            "status": "OPEN",
            "priority": "Medium"
        }
    )

    assert response.status_code == 201
    complaint_id = response.json()["complaint_id"]

    # Step 2: Retrieve the initial complaint history
    history_response = client.get("/events")

    assert history_response.status_code == 200

    events = [
        event for event in history_response.json()
        if event["complaint_id"] == complaint_id
    ]

    assert len(events) == 1
    assert events[0]["new_status"] == "OPEN"

    # Step 3: Update the complaint status
    update_response = client.patch(
        f"/complaints/{complaint_id}/status",
        json={"new_status": "IN_PROGRESS"}
    )

    assert update_response.status_code == 200

    # Step 4: Verify the updated history
    history_response = client.get("/events")

    assert history_response.status_code == 200

    events = [
        event for event in history_response.json()
        if event["complaint_id"] == complaint_id
    ]

    assert len(events) == 2

    # Step 5: Verify the transaction in SQLite
    test_db.expire_all()

    complaint = test_db.get(Complaint, complaint_id)

    assert complaint.status.value == "IN_PROGRESS"

    saved_events = (
        test_db.query(ComplaintStatusEvent)
        .filter_by(complaint_id=complaint_id)
        .order_by(ComplaintStatusEvent.history_id)
        .all()
    )

    assert len(saved_events) == 2

    assert saved_events[0].old_status is None
    assert saved_events[0].new_status == "OPEN"

    assert saved_events[1].old_status == "OPEN"
    assert saved_events[1].new_status == "IN_PROGRESS"



def test_week3_release_invalid_status_transition(client, test_db):
    # Step 1: Create a complaint
    response = client.post(
        "/complaints",
        json={
            "customer_id": "CUS001",
            "account_id": "ACC001",
            "channel": "Online",
            "category": "Fee Dispute",
            "complaint_text": "Incorrect fee charged",
            "status": "OPEN",
            "priority": "Medium"
        }
    )

    assert response.status_code == 201
    complaint_id = response.json()["complaint_id"]

    # Step 2: Attempt an invalid status transition
    update_response = client.patch(
        f"/complaints/{complaint_id}/status",
        json={"new_status": "CLOSED"}
    )

    assert update_response.status_code == 409
    assert update_response.json()["code"] == "INVALID_STATUS_TRANSITION"

    # Step 3: Verify the complaint status was not changed
    test_db.expire_all()

    complaint = test_db.get(Complaint, complaint_id)
    assert complaint.status.value == "OPEN"

    # Step 4: Verify no additional history event was created
    events = (
        test_db.query(ComplaintStatusEvent)
        .filter_by(complaint_id=complaint_id)
        .all()
    )

    assert len(events) == 1
    assert events[0].new_status == "OPEN"
