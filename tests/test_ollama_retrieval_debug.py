
import pytest

from src.rag.retrieval_service import retrieve

def test_ollama_retrieval_debug():

    question = (
        "Who can approve a banking complaint escalation?"
    )

    chunks = retrieve(question, top_k=15)

    print("\n=== RETRIEVED EVIDENCE ===")

    for index, chunk in enumerate(chunks, start=1):

        print(f"\n--- Chunk {index} ---")
        print("Chunk ID:", chunk["chunk_id"])
        print("Score:", chunk["score"])
        print("Source:", chunk["metadata"]["source_id"])
        print("Section:", chunk["metadata"]["section_title"])
        print("Text:", chunk["text"])

    assert isinstance(chunks, list)
