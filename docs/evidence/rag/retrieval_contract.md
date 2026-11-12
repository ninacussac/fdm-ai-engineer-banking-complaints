# Retrieval Service — API Contract

## Overview

The Retrieval Service provides semantic search over the approved banking policy knowledge base.

It uses Google Gemini to generate query embeddings and ChromaDB to retrieve relevant document chunks.

The service supports metadata filtering and optional deterministic reranking.

## Input Contract

**Function:**

```python
retrieve(
    query,
    top_k=3,
    document_type=None,
    effective_version=None,
    access_label=None,
    rerank=False
)
```

| Parameter | Type | Description |
|---|---|---|
| `query` | `str` | User question to search for |
| `top_k` | `int` | Maximum number of results to retrieve (default: 3) |
| `document_type` | `str \| None` | Optional document type filter |
| `effective_version` | `str \| None` | Optional document version filter |
| `access_label` | `str \| None` | Optional access classification filter |
| `rerank` | `bool` | Enable lexical reranking (default: False) |

### Example

```python
results = retrieve(
    query="When is supervisor approval required?",
    top_k=3,
    document_type="Policy",
    access_label="Internal",
    rerank=True
)
```

## Retrieval Process

1. Validate the query and `top_k`.
2. Generate a query embedding using Gemini.
3. Apply optional metadata filters.
4. Search the persistent ChromaDB collection.
5. Return the retrieved chunks with similarity scores and source metadata.
6. Optionally rerank the retrieved results based on word overlap with the query.

## Output Contract

The service returns a list of dictionaries.

Each result contains:

- `chunk_id`: Unique chunk identifier.
- `text`: Retrieved chunk content.
- `score`: Original cosine similarity score.
- `metadata`: Source metadata associated with the chunk.
- `rerank_score`: Word-overlap score, present only when reranking is enabled.

### Example response

```json
[
  {
    "chunk_id": "KB-001#section#0008#structure#0003",
    "text": "Review | Submit to supervisor/specialist when triggered.",
    "score": 0.772,
    "rerank_score": 2,
    "metadata": {
      "source_id": "KB-001",
      "section_title": "Review",
      "document_type": "Policy",
      "effective_version": "3.0",
      "effective_date": "2026-01-01",
      "access_label": "Internal",
      "status": "Approved"
    }
  }
]
```

## Metadata Filters

Supported filters:

- `document_type`
- `effective_version`
- `access_label`

Multiple filters are combined using a logical AND condition.

Only chunks matching all supplied filters are returned.

Filter values must match the stored metadata values.

## Optional Reranking

When `rerank=True`, the service calculates a deterministic score based on the number of words shared between the query and each retrieved chunk.

Results are sorted by `rerank_score` in descending order.

The original vector similarity score remains available in the `score` field.

Reranking only reorders the retrieved candidates. It does not perform a new search over the entire vector database.

## Error Handling

| Scenario | Behavior |
|---|---|
| Empty query | Raises `ValueError("Query cannot be empty")` |
| Invalid `top_k` | Raises `ValueError("top_k must be positive")` |
| No matching chunks | Returns an empty list `[]` |
| Vector store failure | Raises `RuntimeError("Retrieval Service Unavailable")` |

## Limitations

- Semantic relevance depends on the embedding model and indexed documents.
- Cosine similarity scores are not probabilities of factual correctness.
- Lexical reranking does not understand synonyms or policy semantics.
- Metadata filters use exact matches.
- Access labels are filtering criteria; the current retrieval function does not independently authenticate users or authorize their access.

## Dependencies

- Google Gemini Embedding API
- ChromaDB persistent vector index
- `src/rag/embedding_service.py`
- `src/rag/vector_store.py`

## FastAPI Policy Query Contract — Version 1.0

**Endpoint:** `POST /policy/query`

**Purpose:** Generate a grounded policy answer using retrieved banking policy evidence.

### Request

```json
{
  "question": "What triggers immediate specialist escalation?",
  "document_type": "Policy",
  "effective_version": "2.1",
  "access_label": "Restricted"
}
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `question` | `string` | Yes | Policy question; must not be empty |
| `document_type` | `string \| null` | No | Filter by document type |
| `effective_version` | `string \| null` | No | Filter by document version |
| `access_label` | `string \| null` | No | Filter by access classification |

All filters are optional. A request containing only `question` is valid.

### Successful Response

**HTTP 200**

```json
{
  "answer": "Immediate specialist escalation is triggered by unauthorized transactions, stolen cards, identity compromise, or possible personal-data exposure.",
  "supported": true,
  "citations": [
    {
      "document": "Escalation, Approval and Decision Authority Standard",
      "section": "4. Specialist Escalation Triggers",
      "version": "2.1",
      "source_id": "KB-002"
    }
  ],
  "limitations": []
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `answer` | `string` | Generated answer or abstention message |
| `supported` | `boolean` | Whether sufficient policy evidence supports the answer |
| `citations` | `array` | References to supporting documents |
| `limitations` | `array` | Missing information or limitations |

### Error Handling

| HTTP Status | Meaning |
|---|---|
| `400` | Invalid policy query detected by the service |
| `422` | Request validation failed |
| `503` | Policy answer service unavailable |

### Sprint 3 Integration Notes

- Sprint 3 tools should reuse this endpoint instead of rebuilding the RAG pipeline.
- Filters are combined using logical AND.
- The current API does not expose `top_k` or `rerank`; these remain internal retrieval parameters.
- Access-label filtering is not an authorization mechanism. The server must enforce document access permissions before production use.
- The API may return `supported=false` when evidence is insufficient.

**Contract version:** 1.0

**Release:** Week 4 — Sprint 2