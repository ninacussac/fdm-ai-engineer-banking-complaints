
import os
import pytest

from src.rag.answer_service import generate_answer

def test_ollama_answer(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "ollama")

    question = "Who can approve a banking complaint escalation?"

    evidence = """
    Chunk ID: TEST-001
    Source: TEST-POLICY
    Section: Escalation Approval

    Text: The complaint manager must approve
    escalations before they are submitted.
    """

    result = generate_answer(question, evidence)

    print("\nGenerated result:")
    print(result)

    assert isinstance(result, dict)
    assert isinstance(result["answer"], str)
    assert isinstance(result["supported"], bool)
    assert isinstance(result["citations"], list)
    assert isinstance(result["limitations"], list)