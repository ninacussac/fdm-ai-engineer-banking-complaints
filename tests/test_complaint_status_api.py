
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_invalid_status():
    response = client.patch("/complaints/CMP016/status", json={"new_status":"INVALID_STATUS"})
    assert response.status_code==422

def test_complaint_not_found():
    response = client.patch("/complaints/CMP99999/status", json={"new_status":"IN_PROGRESS"})
    assert response.status_code==404

def test_invalid_transition():
    response = client.patch("/complaints/CMP016/status", json={"new_status":"OPEN"})
    assert response.status_code==409