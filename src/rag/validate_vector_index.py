import json
from vector_store import get_all_vectors

with open("data/processed/chunks_selected.jsonl", "r", encoding="utf-8") as file :
    chunks = [json.loads(line) for line in file]

data = get_all_vectors()

ids = data["ids"]
embeddings = data["embeddings"]
metadatas = data["metadatas"]

expected_ids = {chunk["chunk_id"] for chunk in chunks}
stored_ids = set(ids)

validate_dim = sum(len(embedding)!=3072
                   for embedding in embeddings)

print(validate_dim)

missing_metadata = sum(
    not metadatas
    or not metadata.get("chunk_id")
    or not metadata.get("source_id")
    or not metadata.get("section_title")
    for metadata in metadatas
)
print(missing_metadata)

# Create validation report
report = {
    "chunk_count": len(chunks),
    "vector_count": len(ids),
    "dimensions": 3072,
    "invalid_dimensions": validate_dim,
    "missing_metadata": missing_metadata,
    "duplicate_ids": len(ids) - len(stored_ids),
    "missing_vectors": len(expected_ids - stored_ids),
    "unexpected_vectors": len(stored_ids - expected_ids)
}

report["status"] = (
    "PASS"
    if report["chunk_count"] == report["vector_count"]
    and validate_dim == 0
    and missing_metadata == 0
    and report["duplicate_ids"] == 0
    and report["missing_vectors"] == 0
    and report["unexpected_vectors"] == 0
    else "FAIL"
)

# Save validation report
with open("vector_index_validation.json", "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print(json.dumps(report, indent=4))