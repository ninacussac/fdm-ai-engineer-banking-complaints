
import json
from src.rag.retrieval_service import retrieve


# Load the FDM test cases
with open("tests/data/retrieval_test_set.json", "r", encoding="utf-8") as file:
    test_cases = json.load(file)

sample_results = []

for case in test_cases:
    print("Running:", case["case_id"])

    # Retrieve relevant chunks
    results = retrieve(
        query=case["query"],
        top_k=5,
        document_type=case["filter"].get("document_type"),
        effective_version=case["filter"].get("effective_version"),
        access_label=case["filter"].get("access_label"),
        rerank=True
    )

    # Check whether an expected source was retrieved
    retrieved_sources = [
        result["metadata"]["source_id"]
        for result in results
    ]

    success = any(
        source_id in retrieved_sources
        for source_id in case["expected_source_ids"]
    )

    sample_results.append({
        "case_id": case["case_id"],
        "query": case["query"],
        "filters": case["filter"],
        "expected_source_ids": case["expected_source_ids"],
        "retrieved_source_ids": retrieved_sources,
        "hit_at_5": success,
        "results": results
    })

    print("Hit@5:", success)


# Save the results
with open("retrieval_sample_results.json", "w", encoding="utf-8") as file:
    json.dump(sample_results, file, indent=4, ensure_ascii=False)

print("Results saved to retrieval_sample_results.json")
