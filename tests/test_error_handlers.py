from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError
from src.main import app
from src.api.complaint_router import service_complaint
from uuid import uuid4
import logging


client = TestClient(app)


def test_complaint_not_found_error():
    response = client.get("/complaints/CMP9999")

    assert response.status_code == 404
    assert response.json()["code"] == "COMPLAINT_NOT_FOUND"
    assert response.json()["message"] == "Complaint not found"
    assert "correlation_id" in response.json()
    correlation_id = response.json()["correlation_id"]
    assert correlation_id is not None
    assert correlation_id == response.headers["X-Correlation-ID"]


def test_validation_error():
    response = client.patch("/complaints/CMP016/status", 
                           json = {"new_status":"UNKNOWN"})
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR" 
    assert response.json()["message"] == "Invalid request data"


def test_customer_not_found_error():
    response = client.get("/customers/CUS9999")

    assert response.status_code == 404
    assert response.json()["code"]=="CUSTOMER_NOT_FOUND"
    assert response.json()["message"] == "Customer not found"

#monkeypatch est gere par pytest, objet qui effectue des remplacements temporaires
def test_database_unavailable(monkeypatch):

    def fake_create(db, complaint):
        raise OperationalError("Database unavailable", None, None)

    #remplace le create complainte de service complaint par fake_create
    monkeypatch.setattr(
        service_complaint,
        "create_complaint",
        fake_create
    )

    response = client.post("/complaints/", 
                           json = {
                               "customer_id":"CUS001",
                                "account_id":"ACC001",
                                "channel":"Email",
                                "category":"Fee Dispute",
                                "complaint_text":"database unavailable test",
                                "priority":"Medium",
                                "status":"OPEN"
                           })

    assert response.status_code == 503
    assert response.json()["code"]=="DEPENDENCY_UNAVAILABLE"
    assert response.json()["message"]=="Database unavailable"


def test_correlation_id_propagation():
    correlation_id = str(uuid4())

    response = client.get(
        "/complaints/CMP9999",
        headers={"X-Correlation-ID":correlation_id}
    )

    assert response.status_code==404
    assert response.json()["correlation_id"]==correlation_id
    assert response.headers["X-Correlation-ID"]==correlation_id

#caplog sert a capturer les messages du systeme logging pendant un test
def test_correlation_id_in_logs(caplog):
    correlation_id = str(uuid4())
    #demande a pytest de capturer les logs de notre logger banking_api
    with caplog.at_level(logging.INFO, logger="banking_api"):
        response = client.get("/complaints/CMP9999", 
                              headers={"X-Correlation-ID":correlation_id})

    assert response.status_code==404
    assert response.json()["correlation_id"]==correlation_id
    assert correlation_id in caplog.text
    assert "GET /complaints/{complaint_id}" in caplog.text

def test_sensitive_data_not_logged(caplog):
    sensitive_text = "CONFIDENTIAL_COMPLAINT_TEXT"

    with caplog.at_level(logging.INFO, logger="banking_api"):
        response = client.post(
            "/complaints",
            json={
                "customer_id": "CUS9999",
                "channel": "Online",
                "category": "Fee Dispute",
                "complaint_text": sensitive_text,
                "status": "OPEN",
                "priority": "Medium"
            }
        )
    assert response.status_code==422
    assert sensitive_text not in caplog.text