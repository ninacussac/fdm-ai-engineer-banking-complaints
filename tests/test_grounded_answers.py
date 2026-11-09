from unittest.mock import patch
from src.rag.answer_service import answer_question


def test_unsupported_question():
    # Simulate retrieval without relevant evidence
    with patch("src.rag.answer_service.retrieve", return_value=[]):

        result = answer_question(
            "What is the current weather in Reykjavik?"
        )

    assert result["supported"] is False
    assert result["citations"] == []
    assert len(result["limitations"]) > 0



def test_supported_question():
    # Simulate a relevant retrieved chunk
    chunks = [
        {
            "chunk_id": "chunk-001",
            "text": "Supervisor approval is required above CAD 1,000.",
            "score": 0.85,
            "metadata": {
                "title": "Complaint Approval Policy",
                "section_title": "3. Financial Redress Thresholds",
                "effective_version": "2.1",
                "source_id": "KB-002"
            }
        }
    ]

    # Simulate Gemini's response
    generated_answer = {
        "answer": "Supervisor approval is required above CAD 1,000.",
        "supported": True,
        "citations": ["chunk-001"],
        "limitations": []
    }

    with patch("src.rag.answer_service.retrieve", return_value=chunks):
        with patch("src.rag.answer_service.generate_answer", return_value=generated_answer):
            result = answer_question(
                "When does proposed compensation require supervisor approval?"
            )

    assert result["supported"] is True
    assert result["citations"][0]["source_id"] == "KB-002"
    assert result["limitations"] == []



def test_partially_supported_question():
    # Simulate a relevant policy chunk
    chunks = [
        {
            "chunk_id": "chunk-001",
            "text": "Supervisor approval is required above CAD 1,000.",
            "score": 0.85,
            "metadata": {
                "title": "Complaint Approval Policy",
                "section_title": "3. Financial Redress Thresholds",
                "effective_version": "2.1",
                "source_id": "KB-002"
            }
        }
    ]

    # Simulate a partially supported Gemini answer
    generated_answer = {
        "answer": "Supervisor approval is required above CAD 1,000.",
        "supported": True,
        "citations": ["chunk-001"],
        "limitations": [
            "The supplied knowledge base does not provide current weather information."
        ]
    }

    with patch("src.rag.answer_service.retrieve", return_value=chunks):
        with patch("src.rag.answer_service.generate_answer", return_value=generated_answer):
            result = answer_question(
                "When does proposed compensation require supervisor approval, "
                "and what is the current weather in Reykjavik?"
            )

    assert result["supported"] is True
    assert result["citations"][0]["source_id"] == "KB-002"
    assert len(result["limitations"]) > 0
    assert "weather" in result["limitations"][0].lower()
