
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Same question for both pipelines
QUESTIONS = [
    "What approvals are required for a proposed complaint compensation of exactly CAD 10,000?",

    "What approvals are required when a proposed complaint compensation exceeds CAD 10,000?",

    "What is the bank's policy for cryptocurrency mining rewards?",

    "What information must an approval request contain?",
]

# Each pipeline runs in a separate Python process
PIPELINES = {
    "Gemini RAG": {
        "EMBEDDING_PROVIDER": "gemini",
        "LLM_PROVIDER": "gemini",
    },
    "Ollama RAG": {
        "EMBEDDING_PROVIDER": "ollama",
        "LLM_PROVIDER": "ollama",
        "OLLAMA_MODEL": "qwen3:4b",
        "OLLAMA_EMBEDDING_MODEL": "nomic-embed-text",
    },
}

# Executed independently for each pipeline
RAG_SCRIPT = """
import json
from src.rag.answer_service import answer_question

question = json.loads(__import__("sys").argv[1])
result = answer_question(question)

print("RAG_RESULT_JSON:" + json.dumps(result, ensure_ascii=False))
"""


def run_rag(question, config):
    env = os.environ.copy()
    env.update(config)

    start = time.perf_counter()

    process = subprocess.run(
        [sys.executable, "-c", RAG_SCRIPT, json.dumps(question)],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
    )

    duration = time.perf_counter() - start

    if process.returncode != 0:
        pytest.fail(
            f"RAG execution failed:\n{process.stderr}\n{process.stdout}"
        )

    marker = "RAG_RESULT_JSON:"
    result_line = next(
        (
            line for line in process.stdout.splitlines()
            if line.startswith(marker)
        ),
        None,
    )

    if result_line is None:
        pytest.fail(
            f"No JSON result found:\n{process.stdout}"
        )

    result = json.loads(result_line[len(marker):])

    return result, duration


@pytest.mark.parametrize("question", QUESTIONS)
def test_compare_gemini_and_ollama(question):

    results = {}

    print("\n" + "=" * 75)
    print("QUESTION:", question)
    print("=" * 75)

    for name, config in PIPELINES.items():
        result, duration = run_rag(question, config)
        results[name] = result

        print(f"\n--- {name} ---")
        print("Answer:", result["answer"])
        print("Supported:", result["supported"])
        print("Citations:")
        for citation in result["citations"]:
            print(" ", citation)
        print("Limitations:", result["limitations"])
        print(f"Duration: {duration:.2f}s")

        # Technical validation
        assert isinstance(result["answer"], str)
        assert isinstance(result["supported"], bool)
        assert isinstance(result["citations"], list)
        assert isinstance(result["limitations"], list)

    gemini = results["Gemini RAG"]
    ollama = results["Ollama RAG"]

    print("\n--- COMPARISON ---")
    print("Same answer:", gemini["answer"] == ollama["answer"])
    print("Same supported status:",
          gemini["supported"] == ollama["supported"])
    print("Gemini citations:", len(gemini["citations"]))
    print("Ollama citations:", len(ollama["citations"]))
    print("=" * 75)