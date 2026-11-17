def format_citations(citation_ids, evidence):
    citations = []

    for chunk_id in citation_ids:
        # Find the cited chunk in retrieved evidence
        chunk = next(
            (item for item in evidence if item["chunk_id"] == chunk_id),
            None
        )

        # Reject citations not found in retrieved evidence
        if chunk is None:
            raise ValueError(f"Invalid citation: {chunk_id}")

        metadata = chunk["metadata"]

        citation = {
            "document": metadata["title"],
            "section": metadata["section_title"],
            "version": metadata["effective_version"],
            "source_id": metadata["source_id"]
        }

        if citation not in citations:
            citations.append(citation)

    return citations

if __name__ == "__main__":
    evidence = [
        {
            "chunk_id": "chunk-001",
            "metadata": {
                "title": "Complaint Policy",
                "section_title": "3. Financial Redress Thresholds",
                "effective_version": "2.1",
                "source_id": "KB-002"
            }
        }
    ]

    # Test an invalid citation
    print(format_citations(["chunk-999"], evidence))