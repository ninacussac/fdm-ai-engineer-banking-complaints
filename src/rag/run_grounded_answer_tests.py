
import json
from src.rag.answer_service import answer_question

# Load FDM test cases
with open("tests/data/grounded_answer_cases.json", encoding="utf-8") as file:
    test_cases = json.load(file)

results = []

for case in test_cases:
    print("Running:", case["case_id"])

    # Generate the answer using the RAG pipeline
    answer = answer_question(case["question"])

    # Save the test case and generated answer
    results.append({
        "case_id": case["case_id"],
        "question": case["question"],
        "expected_support_level": case["expected_support_level"],
        "expected_source_id": case["expected_source_id"],
        "response": answer
    })

    print("Supported:", answer["supported"])
    print("Citations:", len(answer["citations"]))
    print("------------------------")

# Save results
with open("grounded_answer_results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)

print("Results saved to grounded_answer_results.json")
