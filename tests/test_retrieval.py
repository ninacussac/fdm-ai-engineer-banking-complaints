import pytest
from unittest.mock import patch
from src.rag.retrieval_service import retrieve


def test_empty_query():
    with pytest.raises(ValueError, match="Query cannot be empty"):
        retrieve("")

def test_no_matches():
    # Simulate an empty response from ChromaDB
    empty_response = {
        "ids": [[]],
        "documents": [[]],
        "metadatas": [[]],
        "distances": [[]]
    }

    with patch("src.rag.retrieval_service.get_gemini_embedding") as mock_embedding:
        with patch("src.rag.retrieval_service.search_vectors", return_value=empty_response):

            mock_embedding.return_value = [0.1, 0.2, 0.3]

            results = retrieve("Unknown banking policy")

    assert results == []


def test_vector_store_unavailable():

    with patch("src.rag.retrieval_service.get_gemini_embedding") as mock_embedding:
        with patch("src.rag.retrieval_service.search_vectors") as mock_search:

            # Simulate a valid query embedding
            mock_embedding.return_value = [0.1, 0.2, 0.3]

            # Simulate a ChromaDB failure
            mock_search.side_effect = Exception("ChromaDB connection failed")

            with pytest.raises(RuntimeError, match="Retrieval Service Unavailable"):
                retrieve("When is supervisor approval required?")