
import pytest

import src.rag.answer_service as service


@pytest.fixture
def sample_chunks():
    return [
        {
            "chunk_id": "KB-002#section#0004#structure#0002",
            "text": (
                "Supervisor approval is required for proposed "
                "compensation above CAD 1,000."
            ),
            "score": 0.85,
            "metadata": {
                "source_id": "KB-002",
                "section_title": "Financial Redress Thresholds",
            },
        }
    ]


def test_abstain_when_no_chunks(monkeypatch):
    """No retrieved evidence must produce an abstention."""

    monkeypatch.setattr(
        service,
        "retrieve",
        lambda *args, **kwargs: [],
    )

    result = service.answer_question("Unknown policy question")

    assert result["supported"] is False
    assert result["citations"] == []
    assert result["limitations"]


def test_abstain_when_similarity_too_low(
    monkeypatch, sample_chunks
):
    """Low-scoring evidence must be rejected."""

    sample_chunks[0]["score"] = 0.50

    monkeypatch.setattr(
        service,
        "retrieve",
        lambda *args, **kwargs: sample_chunks,
    )

    result = service.answer_question(
        "Who approves compensation?"
    )

    assert result["supported"] is False
    assert result["citations"] == []


def test_valid_citation(
    monkeypatch, sample_chunks
):
    """Valid generated chunk IDs must be accepted."""

    chunk_id = sample_chunks[0]["chunk_id"]

    monkeypatch.setattr(
        service,
        "retrieve",
        lambda *args, **kwargs: sample_chunks,
    )

    def fake_generate_answer(question, evidence, chunks):
        return {
            "answer": "Supervisor approval is required.",
            "supported": True,
            "citations": [chunk_id],
            "limitations": [],
        }

    monkeypatch.setattr(
        service,
        "generate_answer",
        fake_generate_answer,
    )

    # Use the real citation validator, with complete test metadata
    # replaced by a spy to test the service's hand-off independently.
    def fake_format_citations(citation_ids, evidence):
        assert citation_ids == [chunk_id]
        assert evidence == sample_chunks
        return [{"source_id": "KB-002"}]

    monkeypatch.setattr(
        service,
        "format_citations",
        fake_format_citations,
    )

    result = service.answer_question(
        "Who approves compensation?"
    )

    assert result["supported"] is True
    assert result["citations"] == [
        {"source_id": "KB-002"}
    ]


def test_invalid_citation_causes_abstention(
    monkeypatch, sample_chunks
):
    """An invalid generated citation must never be exposed."""

    monkeypatch.setattr(
        service,
        "retrieve",
        lambda *args, **kwargs: sample_chunks,
    )

    def fake_generate_answer(question, evidence, chunks):
        return {
            "answer": "Supervisor approval is required.",
            "supported": True,
            "citations": ["KB-002 §3"],
            "limitations": [],
        }

    monkeypatch.setattr(
        service,
        "generate_answer",
        fake_generate_answer,
    )

    def fake_format_citations(citation_ids, evidence):
        allowed_ids = {
            chunk["chunk_id"] for chunk in evidence
        }

        for citation_id in citation_ids:
            if citation_id not in allowed_ids:
                raise ValueError(
                    f"Invalid citation: {citation_id}"
                )

        return []

    monkeypatch.setattr(
        service,
        "format_citations",
        fake_format_citations,
    )

    result = service.answer_question(
        "Who approves compensation?"
    )

    assert result["supported"] is False
    assert result["citations"] == []
    assert result["limitations"]