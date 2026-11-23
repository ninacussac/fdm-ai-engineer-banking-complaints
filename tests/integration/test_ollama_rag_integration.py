
import pytest

from src.rag.answer_service import answer_question


@pytest.mark.parametrize(
    "question, expected_supported, expected_terms, forbidden_terms",
    [
        (
            "What approvals are required when a proposed "
            "complaint compensation exceeds CAD 10,000?",
            True,
            ["supervisor", "senior"],
            [],
        ),
        (
            "What approvals are required for a proposed "
            "complaint compensation of exactly CAD 10,000?",
            True,
            ["supervisor"],
            ["senior escalation is required",
             "senior escalation and supervisor approval are required"],
        ),
        (
            "What is the bank's policy for cryptocurrency "
            "mining rewards?",
            False,
            [],
            [],
        ),
    ],
)
def test_ollama_rag_scenarios(
    question,
    expected_supported,
    expected_terms,
    forbidden_terms,
):

    result = answer_question(question)

    print("\nQUESTION:", question)
    print("ANSWER:", result["answer"])
    print("SUPPORTED:", result["supported"])
    print("CITATIONS:", result["citations"])
    print("LIMITATIONS:", result["limitations"])

    assert isinstance(result["answer"], str)
    assert isinstance(result["supported"], bool)
    assert isinstance(result["citations"], list)
    assert isinstance(result["limitations"], list)

    assert result["supported"] is expected_supported

    if result["supported"]:
        assert result["citations"]
    else:
        assert result["citations"] == []
        assert result["limitations"]

    answer = result["answer"].lower()

    for term in expected_terms:
        assert term in answer, (
            f"Expected '{term}' in answer: {result['answer']}"
        )

    for term in forbidden_terms:
        assert term not in answer, (
            f"Forbidden statement '{term}' in answer: "
            f"{result['answer']}"
        )