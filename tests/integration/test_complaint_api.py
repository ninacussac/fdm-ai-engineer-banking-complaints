from sqlalchemy.exc import OperationalError
from sqlalchemy import event

from src.api.complaint_router import service_complaint
from src.models.models import Complaint, ComplaintStatusEvent


def test_create_complaint(client, test_db):
    response = client.post("/complaints", 
                           json=
                           {
                               "customer_id":"CUS001",
                               "account_id": "ACC001",
                                "channel": "Online",
                                "category": "Fee Dispute",
                                "complaint_text": "Incorrect fee charged",
                                "status": "OPEN",
                                "priority": "Medium"
                           })
    #API a bien accepete la creation de la plainte
    assert response.status_code==201

    complaint_id = response.json()["complaint_id"]
    #interroge directement la base de donnees temporaire pourvoir si la plainte existe
    saved_complaint = test_db.get(Complaint, complaint_id)

    assert saved_complaint.customer_id=="CUS001"
    assert saved_complaint.status.value == "OPEN"

    events = (test_db.query(ComplaintStatusEvent).filter_by(complaint_id = complaint_id).all())

    assert len(events)==1
    assert events[0].old_status is None
    assert events[0].new_status =="OPEN"

def test_valid_complaint_status_update(client,test_db):
    create_response  = client.post("/complaints", 
                                   json=
                                   {
                                       "customer_id":"CUS001",
                                        "account_id": "ACC001",
                                        "channel": "Online",
                                        "category": "Fee Dispute",
                                        "complaint_text": "Incorrect fee charged",
                                        "status": "OPEN",
                                        "priority": "Medium"
                                   })
    assert create_response.status_code==201
    complaint_id = create_response.json()["complaint_id"]

    response = client.patch(f"/complaints/{complaint_id}/status", json = {"new_status":"IN_PROGRESS"})

    assert response.status_code==200

    test_db.expire_all() #oublie les valeurs deja chargees en memoire
    complaint = test_db.get(Complaint, complaint_id)

    assert complaint.status.value == "IN_PROGRESS"

    events = (test_db.query(ComplaintStatusEvent).filter_by(complaint_id=complaint_id).order_by(ComplaintStatusEvent.history_id).all())

    assert len(events)==2
    assert events[1].old_status=="OPEN"
    assert events[1].new_status=="IN_PROGRESS"


def test_create_complaint_with_missing_priority(client, test_db):
    initial_count = test_db.query(Complaint).count()
    create_response  = client.post(
                        "/complaints", 
                        json=
                        {
                            "customer_id":"CUS001",
                            "account_id": "ACC001",
                            "channel": "Online",
                            "category": "Fee Dispute",
                            "complaint_text": "Incorrect fee charged",
                            "status": "OPEN",
                        })

    assert create_response.status_code==422
    assert create_response.json()["code"]=="VALIDATION_ERROR"

    test_db.expire_all()
    final_count = test_db.query(Complaint).count()
    assert final_count==initial_count


def test_invalid_complaint_status_update(client,test_db):
    create_response  = client.post("/complaints", 
                                   json=
                                   {
                                       "customer_id":"CUS001",
                                        "account_id": "ACC001",
                                        "channel": "Online",
                                        "category": "Fee Dispute",
                                        "complaint_text": "Incorrect fee charged",
                                        "status": "OPEN",
                                        "priority": "Medium"
                                   })
    assert create_response.status_code==201
    complaint_id = create_response.json()["complaint_id"]

    result = client.patch(f"/complaints/{complaint_id}/status", json = {"new_status":"CLOSED"})

    assert result.status_code == 409
    assert result.json()["code"]=="INVALID_STATUS_TRANSITION"

    test_db.expire_all()
    saved_complaint = test_db.get(Complaint, complaint_id)
    assert saved_complaint.status=="OPEN"

    events = test_db.query(ComplaintStatusEvent).filter_by(complaint_id=complaint_id).all()
    assert len(events)==1

def test_database_unavailable(client, monkeypatch):
    def fake_create_complaint(db,complaint):
        # args : la requete qui echoue, les param transmis a cette requete, et l'erreur que l'on souhaite simuler
        raise OperationalError(
            "INSERT INTO complaint", {}, Exception("Database unavailable")
        )
    
    monkeypatch.setattr(service_complaint, "create_complaint", fake_create_complaint)

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

    assert response.status_code == 503
    assert response.json()["code"]=="DEPENDENCY_UNAVAILABLE"
    assert response.json()["message"]=="Database unavailable"



def test_rollback_when_status_event_fails(client, test_db):
    initial_count = test_db.query(Complaint).count()

    def fail_event_insert(mapper, connection, target):
        raise RuntimeError("Simulated event failure")

    #permet d'executer une fonction lorsqu'un evenement SQLAlchemy se produit
    event.listen(ComplaintStatusEvent, "before_insert", fail_event_insert)

    try:
        response = client.post(
            "/complaints",
            json={
                "customer_id": "CUS001",
                "account_id": "ACC001",
                "channel": "Online",
                "category": "Fee Dispute",
                "complaint_text": "Rollback test",
                "status": "OPEN",
                "priority": "Medium"
            }
        )
        assert response.status_code==500
        assert response.json()["code"]=="INTERNAL_ERROR"
    finally:
        event.remove(ComplaintStatusEvent, "before_insert", fail_event_insert)

    test_db.expire_all()
    final_count = test_db.query(Complaint).count()
    assert final_count==initial_count


def test_missing_complaint_has_correlation_id(client):
    response = client.get("/complaints/CMP9999")

    assert response.status_code==404
    data = response.json()

    assert data["code"]=="COMPLAINT_NOT_FOUND"
    assert data["message"]=="Complaint not found"

    assert data["correlation_id"] is not None
    assert data["correlation_id"]==response.headers["X-Correlation-ID"]


def test_create_complaint_with_unknown_customer(client, test_db):
    response = client.post(
        "/complaints",
        json={
            "customer_id": "CUS999",
            "channel": "Email",
            "category": "Fee Dispute",
            "complaint_text": "I am unhappy with the banking service.",
            "status": "OPEN",
            "priority": "High"
        }
    )

    assert response.status_code == 422

    data = response.json()
    assert data["code"] == "INVALID_COMPLAINT_DATA"
    assert data["message"] == "Invalid complaint data"
    assert data["correlation_id"] == response.headers["X-Correlation-ID"]