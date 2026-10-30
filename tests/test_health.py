
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from src.main import app


client = TestClient(app)


def test_liveness():
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_database_available():
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_readiness_database_unavailable():
    with patch("src.api.routers.health.engine") as mock_engine:
        mock_engine.connect.side_effect = OperationalError(
            "SELECT 1",
            {},
            Exception("Simulated database failure")
        )

        response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Database unavailable"
    }


def test_liveness_database_unavailable():
    with patch("src.api.routers.health.engine") as mock_engine:
        mock_engine.connect.side_effect = OperationalError(
            "SELECT 1",
            {},
            Exception("Simulated database failure")
        )

        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}
