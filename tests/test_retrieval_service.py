
import pytest
from src.rag import retrieval_service


# Fake response from ChromaDB
def fake_search_vectors(embedding, top_k, filters=None):
    return {
        "ids": [["chunk-1", "chunk-2"]],
        "documents": [[
            "Supervisor approval is required",
            "Complaint escalation procedure"
        ]],
        "distances": [[0.2, 0.4]],
        "metadatas": [[
            {"source_id": "KB-002"},
            {"source_id": "KB-001"}
        ]]
    }


def setup_mocks(monkeypatch):
    # Replace the Gemini API call
    monkeypatch.setattr(retrieval_service,"get_gemini_embedding",lambda query: [0.1, 0.2, 0.3])

    # Replace the ChromaDB call
    monkeypatch.setattr(retrieval_service,"search_vectors",fake_search_vectors)


def test_empty_query():
    with pytest.raises(ValueError, match="Query cannot be empty"):
        retrieval_service.retrieve("   ")


def test_invalid_top_k():
    with pytest.raises(ValueError, match="top_k must be positive"):
        retrieval_service.retrieve("Complaint escalation", top_k=0)


def test_retrieve_results(monkeypatch):
    setup_mocks(monkeypatch)

    results = retrieval_service.retrieve("Complaint escalation")

    assert len(results) == 2
    assert results[0]["chunk_id"] == "chunk-1"
    assert results[0]["text"] == "Supervisor approval is required"
    assert results[0]["score"] == 0.8
    assert results[0]["metadata"]["source_id"] == "KB-002"


def test_single_filter(monkeypatch):
    setup_mocks(monkeypatch)

    # Capture filters passed to ChromaDB
    captured = {}

    def fake_search(embedding, top_k, filters=None):
        captured["filters"] = filters
        return fake_search_vectors(embedding, top_k, filters)

    monkeypatch.setattr(retrieval_service, "search_vectors", fake_search)

    retrieval_service.retrieve(
        "Complaint escalation",
        document_type="Policy"
    )

    assert captured["filters"] == {"document_type": "Policy"}


def test_multiple_filters(monkeypatch):
    setup_mocks(monkeypatch)

    captured = {}

    def fake_search(embedding, top_k, filters=None):
        captured["filters"] = filters
        return fake_search_vectors(embedding, top_k, filters)

    monkeypatch.setattr(retrieval_service, "search_vectors", fake_search)

    retrieval_service.retrieve(
        "Complaint escalation",
        document_type="Policy",
        effective_version="2.1",
        access_label="Restricted"
    )

    assert captured["filters"] == {
        "$and": [
            {"document_type": "Policy"},
            {"effective_version": "2.1"},
            {"access_label": "Restricted"}
        ]
    }


def test_no_results(monkeypatch):
    setup_mocks(monkeypatch)

    def fake_empty_search(embedding, top_k, filters=None):
        return {
            "ids": [[]],
            "documents": [[]],
            "distances": [[]],
            "metadatas": [[]]
        }

    monkeypatch.setattr(
        retrieval_service,
        "search_vectors",
        fake_empty_search
    )

    results = retrieval_service.retrieve("Unknown question")

    assert results == []


def test_vector_store_error(monkeypatch):
    setup_mocks(monkeypatch)

    def fake_error(embedding, top_k, filters=None):
        raise Exception("Database error")

    monkeypatch.setattr(
        retrieval_service,
        "search_vectors",
        fake_error
    )

    with pytest.raises(RuntimeError, match="Retrieval Service Unavailable"):
        retrieval_service.retrieve("Complaint escalation")


def test_rerank_results():
    chunks = [
        {"text": "Customer account information"},
        {"text": "Complaint escalation procedure"},
        {"text": "Complaint escalation requires approval"}
    ]

    results = retrieval_service.rerank_results(
        "complaint escalation",
        chunks
    )

    assert results[0]["rerank_score"] == 2
    assert results[1]["rerank_score"] == 2
    assert results[2]["rerank_score"] == 0
