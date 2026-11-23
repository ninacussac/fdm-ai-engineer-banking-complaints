
import pytest
from types import SimpleNamespace
from src.agents import tools
from datetime import datetime

def test_get_customer(monkeypatch):
    # Simulate a customer returned by SQLAlchemy
    fake_customer = SimpleNamespace(
        customer_id="CUS001",
        first_name="Damien",
        last_name="Reynier",
        segment=None,
    )

    # Simulate the repository
    class FakeCustomerRepository:
        def get_by_id(self, db, customer_id):
            assert customer_id == "CUS001"
            return fake_customer

    # Simulate the database session
    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    monkeypatch.setattr(
        tools,
        "CustomerRepository",
        FakeCustomerRepository
    )

    monkeypatch.setattr(
        tools,
        "SessionLocal",
        FakeSession
    )

    result = tools.get_customer("CUS001")

    assert result == {
        "customer_id": "CUS001",
        "first_name": "Damien",
        "last_name": "Reynier",
        "segment": None,
    }


def test_get_accounts(monkeypatch):
    fake_accounts = [
        SimpleNamespace(
            account_id="ACC001",
            customer_id="CUS001",
            account_type="Chequing",
            status="ACTIVE",
        ),
        SimpleNamespace(
            account_id="ACC002",
            customer_id="CUS001",
            account_type="Savings",
            status="ACTIVE",
        ),
    ]

    class FakeAccountRepository:
        def get_for_customer(self, db, customer_id):
            assert customer_id == "CUS001"
            return fake_accounts

    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    monkeypatch.setattr(
        tools,
        "AccountRepository",
        FakeAccountRepository
    )

    monkeypatch.setattr(
        tools,
        "SessionLocal",
        FakeSession
    )

    result = tools.get_accounts("CUS001")

    assert len(result) == 2
    assert result[0]["account_id"] == "ACC001"
    assert result[1]["account_id"] == "ACC002"
    assert all(account["customer_id"] == "CUS001" for account in result)



def test_get_complaint(monkeypatch):
    fake_complaint = SimpleNamespace(
        complaint_id="CMP001",
        customer_id="CUS001",
        account_id="ACC001",
        category=SimpleNamespace(value="Fee Dispute"),
        status=SimpleNamespace(value="OPEN"),
        priority=SimpleNamespace(value="High"),
        received_at=datetime(2026, 10, 29, 19, 13, 52),
    )

    class FakeComplaintRepository:
        def get_by_id(self, db, complaint_id):
            assert complaint_id == "CMP001"
            return fake_complaint

    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    monkeypatch.setattr(
        tools,
        "ComplaintRepository",
        FakeComplaintRepository
    )

    monkeypatch.setattr(
        tools,
        "SessionLocal",
        FakeSession
    )

    result = tools.get_complaint("CMP001")

    assert result["complaint_id"] == "CMP001"
    assert result["customer_id"] == "CUS001"
    assert result["account_id"] == "ACC001"
    assert result["category"] == "Fee Dispute"
    assert result["status"] == "OPEN"
    assert result["priority"] == "High"
    assert result["received_at"] == "2026-10-29T19:13:52"



def test_search_policy(monkeypatch):
    # Simulate retrieved policy chunks
    fake_results = [
        {
            "chunk_id": "KB-003#section#0002#structure#0001",
            "text": "Covers monthly account fees and service charges.",
            "score": 0.85,
            "metadata": {
                "source_id": "KB-003",
                "document_type": "Playbook",
                "status": "Approved",
                "access_label": "Internal",
            },
        }
    ]

    def fake_retrieve(**kwargs):
        assert kwargs["query"] == "What is the policy for bank fees?"
        assert kwargs["top_k"] == 3
        assert kwargs["access_label"] == "Internal"
        return fake_results

    monkeypatch.setattr(tools, "retrieve", fake_retrieve)

    result = tools.search_policy(
        query="What is the policy for bank fees?",
        filters={"access_label": "Internal"},
        top_k=3,
    )

    assert len(result) == 1
    assert result[0]["metadata"]["source_id"] == "KB-003"
    assert result[0]["metadata"]["status"] == "Approved"
    assert result[0]["metadata"]["access_label"] == "Internal"


@pytest.mark.parametrize(
    "function, argument",
    [
        (tools.get_customer, ""),
        (tools.get_accounts, ""),
        (tools.get_complaint, ""),
        (tools.search_policy, ""),
    ],
)
def test_empty_input(function, argument):
    with pytest.raises(ValueError):
        function(argument)


def test_invalid_top_k():
    with pytest.raises(ValueError):
        tools.search_policy("Complaint policy", top_k=0)


def test_invalid_policy_filter():
    with pytest.raises(ValueError):
        tools.search_policy(
            "Complaint policy",
            filters={"unknown_filter": "value"}
        )

def test_get_customer_not_found(monkeypatch):

    class FakeCustomerRepository:
        def get_by_id(self, db, customer_id):
            return None

    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    monkeypatch.setattr(
        tools,
        "CustomerRepository",
        FakeCustomerRepository
    )

    monkeypatch.setattr(
        tools,
        "SessionLocal",
        FakeSession
    )

    result = tools.get_customer("CUS999")

    assert result is None



def test_get_complaint_not_found(monkeypatch):

    class FakeComplaintRepository:
        def get_by_id(self, db, complaint_id):
            assert complaint_id == "CMP999"
            return None

    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    monkeypatch.setattr(
        tools,
        "ComplaintRepository",
        FakeComplaintRepository
    )

    monkeypatch.setattr(
        tools,
        "SessionLocal",
        FakeSession
    )

    result = tools.get_complaint("CMP999")

    assert result is None


def test_get_accounts_empty(monkeypatch):

    class FakeAccountRepository:
        def get_for_customer(self, db, customer_id):
            assert customer_id == "CUS999"
            return []

    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    monkeypatch.setattr(
        tools,
        "AccountRepository",
        FakeAccountRepository
    )

    monkeypatch.setattr(
        tools,
        "SessionLocal",
        FakeSession
    )

    result = tools.get_accounts("CUS999")

    assert result == []



def test_get_customer_db_failure(monkeypatch):

    class FakeCustomerRepository:
        def get_by_id(self, db, customer_id):
            raise ConnectionError("Database unavailable")

    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    monkeypatch.setattr(
        tools,
        "CustomerRepository",
        FakeCustomerRepository
    )

    monkeypatch.setattr(
        tools,
        "SessionLocal",
        FakeSession
    )

    with pytest.raises(ConnectionError, match="Database unavailable"):
        tools.get_customer("CUS001")


def test_search_policy_failure(monkeypatch):

    def fake_retrieve(**kwargs):
        raise RuntimeError("Retrieval Service Unavailable")

    monkeypatch.setattr(
        tools,
        "retrieve",
        fake_retrieve
    )

    with pytest.raises(
        RuntimeError,
        match="Retrieval Service Unavailable"
    ):
        tools.search_policy(
            "What is the policy for disputing bank fees?",
            top_k=3
        )


def test_search_policy_no_results(monkeypatch):

    def fake_retrieve(**kwargs):
        assert kwargs["query"] == "Unknown banking policy"
        assert kwargs["top_k"] == 3
        return []

    monkeypatch.setattr(
        tools,
        "retrieve",
        fake_retrieve
    )

    result = tools.search_policy(
        query="Unknown banking policy",
        top_k=3
    )

    assert result == []


def test_search_policy_restricted_denied(monkeypatch):

    def fake_retrieve(**kwargs):
        pytest.fail(
            "Retrieval must not run for a denied request"
        )

    monkeypatch.setattr(
        tools,
        "retrieve",
        fake_retrieve
    )

    with pytest.raises(PermissionError):
        tools.search_policy(
            query="Escalation approval policy",
            filters={"access_label": "Restricted"},
        )


def test_retrieval_approved_only(monkeypatch):
    from src.rag import retrieval_service

    captured = {}

    def fake_embedding(query):
        return [0.1, 0.2, 0.3]

    def fake_search_vectors(embedding, top_k, filters=None):
        captured["filters"] = filters

        return {
            "ids": [[]],
            "documents": [[]],
            "distances": [[]],
            "metadatas": [[]],
        }

    monkeypatch.setattr(
        retrieval_service,
        "get_embedding",
        fake_embedding
    )

    monkeypatch.setattr(
        retrieval_service,
        "search_vectors",
        fake_search_vectors
    )

    results = retrieval_service.retrieve(
        query="Bank fee dispute",
        top_k=3,
        access_label="Internal"
    )

    assert results == []

    assert captured["filters"] == {
        "$and": [
            {"status": "Approved"},
            {"access_label": "Internal"}
        ]
    }
