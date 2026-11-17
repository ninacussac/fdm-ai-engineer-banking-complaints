import pytest

from src.rag.answer_service import answer_question

def test_ollama_rag(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER","ollama")
    question = ("What approvals are required when a proposed complaint compensation exceeds CAD 10,000?")

    result = answer_question(question)

    print("\nRAG response")
    print(result)

    assert isinstance(result, dict)
    assert isinstance(result["answer"],str)
    assert isinstance(result["supported"], bool)
    assert isinstance(result["citations"], list)
    assert isinstance(result["limitations"], list)

    if not result["supported"]:
        print("RAG abstained due to insufficient evidence")