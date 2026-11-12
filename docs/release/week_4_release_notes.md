# Week 4 — RAG Release Notes

## 1. Release Overview

This release integrates the Week 4 Policy Knowledge RAG Service with the existing Week 3 Banking Complaint API.

The service retrieves approved banking policy evidence and generates grounded answers with citations.

**Release branch:** `feature/week4-release`

**Release status:** Pending coach review and independent clean setup validation.

## 2. New Features

### Document Ingestion

- DOCX policy document extraction.
- Manifest and metadata validation.
- Approved-document filtering.
- Structured document extraction and chunking.

### Embeddings and Vector Storage

- Gemini embedding generation.
- ChromaDB vector storage.
- Semantic similarity retrieval.
- Retrieval filters for document type, effective version and access label.

### Grounded Answer Generation

- Gemini-generated policy answers.
- Source and section citations.
- Evidence-based abstention when information is insufficient.
- FastAPI endpoint: `POST /policy/query`.

### Evaluation

- Six-case locked golden set.
- Retrieval and answer baseline.
- Human review of citation validity and faithfulness.
- Failure analysis and proposed improvements.

## 3. Integration and Testing

- 92 automated tests passed.
- Four ingestion tests passed.
- Twelve approved documents validated and extracted.
- 175 sections extracted.
- 208 vectors available in the existing ChromaDB index.
- Supported policy questions returned grounded answers with citations.
- A filtered policy query returned HTTP 200 with a matching policy citation.
- `GET /complaints` returned HTTP 200 with complaint records.

**Test evidence:** `evidence/week4/`

**Evaluation report:** `evaluation/evaluation_report.md`

## 4. Evaluation Results

| Metric | Baseline Result |
|---|---|
| Source Hit@5 | 100% |
| Section Hit@5 | 80% |
| Support Classification Accuracy | 83.33% |
| Expected Citation Match | 40% |

These results are based on six evaluation cases and do not represent production acceptance.

## 5. Known Limitations

- Gemini availability is external and intermittent HTTP 503 errors were observed.
- Retrieval does not always identify the expected policy section.
- Generated citations may refer to valid evidence different from the expected reference.
- Existing embeddings are skipped based on chunk IDs; modified chunk content may require explicit reindexing.
- Document access labels are retrieval filters, not independently enforced authorization controls.
- The policy corpus requires authorized distribution outside the Git repository.
- Independent clean setup validation remains pending.

## 6. Sprint 3 Handover

Sprint 3 tools should reuse the existing RAG pipeline rather than rebuilding it.

Integration entry points:

- FastAPI policy endpoint: `POST /policy/query`.
- Retrieval service: `src/rag/retrieval_service.py`.
- Answer service: `src/rag/answer_service.py`.
- Vector store: `src/rag/vector_store.py`.

The retrieval contract will document the supported request parameters and response structure.

## 7. Release Status

The release remains pending until the required checks are completed and the Pull Request has been reviewed by the coach.

No production readiness or independent setup approval is claimed.