import pytest
from ollama import Client

def test_ollama_embeddings():
    client =Client(host="http://localhost:11434")

    texts = [
        "A supervisor must approve certain complaint resolutions.",
        "Senior escalation is required for high-impact complaints.",
    ]

    response = client.embed(model = "nomic-embed-text",
                            input=texts)

    embeddings = response.embeddings

    print("\n Number of embeddings : ", len(embeddings))
    print("Vector dimension : ", len(embeddings[0]))
    print(" First five values : ", embeddings[0][:5])

    assert len(embeddings)==len(texts)
    assert len(embeddings[0])>0
    assert len(embeddings[0])==len(embeddings[1])