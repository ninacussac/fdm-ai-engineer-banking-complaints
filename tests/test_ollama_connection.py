
import pytest
from ollama import Client


OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2:1b"

def test_ollama_connection():
    """Verify that the local Ollama server generates a response."""

    client = Client(host=OLLAMA_URL)

    response = client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a banking policy assistant."
            },
            {
                "role": "user",
                "content": "What is a banking complaint?"
            },
        ],
        options={
            "temperature": 0
        },
    )

    answer = response.message.content

    assert answer is not None
    assert isinstance(answer, str)
    assert len(answer.strip()) > 0

    print("\nOllama response:")
    print(answer)
