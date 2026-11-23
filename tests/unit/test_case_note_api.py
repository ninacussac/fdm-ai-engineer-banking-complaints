
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock

from src.main import app
from src.security.auth import AuthenticatedActor, get_authenticated_actor
from src.services.case_note_service import CaseNoteService

client = TestClient(app)

URL = "/complaints/CMP001/notes"

PAYLOAD = {
    "note": "Customer provided additional evidence.",
    "evidence_refs": ["KB-003"],
}


@pytest.fixture(autouse=True)
def clear_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


def test_create_case_note_unauthenticated():
    response = client.post(URL, json=PAYLOAD)

    assert response.status_code == 401


def test_create_case_note_forbidden_role():
    app.dependency_overrides[get_authenticated_actor] = (
        lambda: AuthenticatedActor(
            actor_id="test_viewer",
            role="Viewer",
        )
    )

    response = client.post(URL, json=PAYLOAD)

    assert response.status_code == 403