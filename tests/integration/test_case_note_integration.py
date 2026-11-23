from datetime import datetime

import pytest
from sqlalchemy import create_engine, select, event, func
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src.data.base import Base
from src.models.models import Customer,Complaint,ComplaintStatus,ComplaintCategory,CaseNote,AuditEvent
from src.services.case_note_service import CaseNoteService
from src.main import app
from src.data.connection import get_db
from src.security.auth import get_authenticated_actor, AuthenticatedActor
from src.config import settings

@pytest.fixture
def db_session(tmp_path):
    # Create a separate SQLite database for this test
    database_path = tmp_path / "test_case_notes.db"

    engine = create_engine(
        f"sqlite:///{database_path}"
    )

    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        # Insert a synthetic customer
        customer = Customer(
            customer_id="CUS001",
            first_name="Test",
            last_name="Customer",
        )

        # Insert a synthetic complaint
        complaint = Complaint(
            complaint_id="CMP001",
            customer_id="CUS001",
            channel="Web",
            category=ComplaintCategory.FEE_DISPUTE,
            complaint_text="Incorrect fee charged.",
            status=ComplaintStatus.OPEN,
            received_at=datetime.now(),
        )

        db.add_all([customer, complaint])
        db.commit()

        yield db

    engine.dispose()


def test_create_case_note_success(db_session):
    service = CaseNoteService()
    result = service.create_case_note(
        db=db_session,
        complaint_id="CMP001",
        note="Customer provided additional evidence.",
        evidence_refs=["KB-003"],
        actor_id="analyst_001",
        actor_role="Analyst",
    )

    assert result["note_id"] is not None
    assert result["audit_id"] is not None

    saved_note = db_session.get(CaseNote, result["note_id"])

    saved_audit = db_session.get(AuditEvent, result["audit_id"])

    assert saved_note is not None
    assert saved_note.complaint_id == "CMP001"
    assert saved_note.note == "Customer provided additional evidence."
    assert saved_note.evidence_refs == ["KB-003"]
    assert saved_note.created_by == "analyst_001"

    assert saved_audit is not None
    assert saved_audit.action == "CREATE_CASE_NOTE"
    assert saved_audit.actor_id == "analyst_001"
    assert saved_audit.complaint_id == "CMP001"
    assert saved_audit.details["note_id"] == saved_note.note_id




def test_create_case_note_rollback(db_session):
    service = CaseNoteService()

    # Simulate a database failure during audit insertion
    def fail_audit_insert(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith("INSERT INTO AUDIT_EVENT"):
            raise RuntimeError("Simulated audit insertion failure")

    event.listen(db_session.bind,"before_cursor_execute",fail_audit_insert)

    try:
        with pytest.raises(RuntimeError, match="Simulated audit insertion failure"):
            service.create_case_note(
                db=db_session,
                complaint_id="CMP001",
                note="Test rollback.",
                evidence_refs=["KB-003"],
                actor_id="analyst_001",
                actor_role="Analyst",
            )
    finally:
        event.remove(db_session.bind,"before_cursor_execute",fail_audit_insert)

    notes = db_session.query(CaseNote).all()
    audits = db_session.query(AuditEvent).all()

    assert len(notes) == 0
    assert len(audits) == 0



def test_analyst_can_create_case_note(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_actor] = (lambda: AuthenticatedActor("analyst_001", "Analyst"))

    try:
        client = TestClient(app)

        response = client.post("/complaints/CMP001/notes",
            json={"note": "Customer provided additional evidence.","evidence_refs": ["KB-003"]})

        assert response.status_code == 201
        result = response.json()

        saved_note = db_session.get(CaseNote, result["note_id"])
        saved_audit = db_session.get(AuditEvent, result["audit_id"])

        assert saved_note is not None
        assert saved_audit is not None
        assert saved_note.created_by == "analyst_001"
        assert saved_audit.action == "CREATE_CASE_NOTE"

    finally:
        app.dependency_overrides.clear()



def test_analyst_can_create_case_note_with_token(db_session,monkeypatch):

    # Configure a synthetic test token
    monkeypatch.setattr(
        settings,
        "BANKING_ANALYST_TOKEN",
        "integration-test-token",
    )

    # Redirect FastAPI to the temporary SQLite database
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            response = client.post(
                "/complaints/CMP001/notes",
                headers={
                    "Authorization": "Bearer integration-test-token"
                },
                json={
                    "note": "Customer provided additional evidence.",
                    "evidence_refs": ["KB-003"],
                },
            )

        assert response.status_code == 201, response.text

        result = response.json()

        saved_note = db_session.get(CaseNote,result["note_id"])

        saved_audit = db_session.get(AuditEvent,result["audit_id"])

        assert saved_note is not None
        assert saved_audit is not None
        assert saved_note.created_by == "analyst_001"
        assert saved_audit.actor_id == "analyst_001"

    finally:
        app.dependency_overrides.pop(get_db, None)
