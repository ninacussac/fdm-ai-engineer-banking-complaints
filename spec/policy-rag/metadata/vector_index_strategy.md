# Complaint Policy RAG — Vector Index Strategy

## 1. Overview

This document defines how policy documents and their chunks will be indexed and retrieved by the Complaint Policy RAG Knowledge Service.

The indexing strategy combines vector search, text search, and metadata filtering to retrieve relevant, approved, and authorized information.

## 2. Vector Index

**Purpose:** Perform semantic similarity search against document chunk embeddings.

The vector index allows the system to retrieve relevant information even when the user's query uses different wording from the original document.

**Indexed content:**
- `chunk_text` — Content represented by its embedding.

**Associated metadata:**
- `chunk_id`
- `source_id`

**Example:**

User query: "How are complaints escalated?"

The query is converted into an embedding and compared with indexed chunk embeddings to retrieve semantically similar passages.

## 3. Text Index

**Purpose:** Support keyword-based and exact-match search.

The text index helps retrieve documents using specific terms, document references, and section headings.

**Indexed fields:**
- `chunk_text`
- `title`
- `section_title`
- `source_id`

**Example:**

User query: "Escalation authority standard"

The system searches for matching keywords in indexed document titles, headings, and content.

Text search complements semantic retrieval when exact terminology is important.

## 4. Metadata Index

Support filtering, document eligibility, access control, and traceability.

**Indexed fields:**

| Field | Purpose |
|---|---|
| `source_id` | Identify the original document. |
| `chunk_id` | Identify the retrieved chunk. |
| `document_type` | Filter by document classification. |
| `version` | Identify the applicable document version. |
| `effective_date` | Determine document applicability. |
| `status` | Identify approved and superseded sources. |
| `access_label` | Enforce access restrictions. |

The field names must remain consistent with `document_metadata_model.md` and the retrieval requirements in `spec.md`.

## 5. Filtering Rules

The retrieval system must apply the following filters:

### 5.1 Document Type Filtering

Use `document_type` to restrict retrieval to the applicable document classifications.

Examples: `Policy`, `Playbook`, `Guide`, `FAQ`, `Casebook`, and `Bulletin`.

### 5.2 Version and Effective Date Filtering

Use `version`, `effective_date`, and `status` to identify the applicable documents.

- Current-policy answers must rely on approved and applicable sources.
- Superseded documents must not be treated as current authoritative evidence.
- Historical retrieval must follow approved business rules.

### 5.3 Access Filtering

Use `access_label` to ensure users only retrieve documents they are authorized to access.

Observed access labels:
- `Internal`
- `Restricted`

**Example:**

Document `KB-002` has `access_label = Restricted`.

If a requesting user is not authorized to access Restricted content, `KB-002` must be excluded from the retrieved evidence, even when its similarity score is high.

Access filtering must use the confirmed role-to-access-label permissions.

## 6. Citation Mapping

**Purpose:** Ensure that generated answers are traceable to their supporting source documents.

Every retrieved chunk must preserve:

- `chunk_id`
- `source_id`
- `section_title`
- `sequence`
- `access_label`

The system must use `source_id` to retrieve the corresponding document title and version.

**Example:**

User query: "What is the escalation procedure for unresolved complaints?"

Retrieved evidence:
- `source_id`: KB-002
- `chunk_id`: KB-002#s3#0002
- `section_title`: 3. Financial Redress Thresholds
- `version`: 2.1

The generated answer must cite the relevant source passage, provided it supports the answer and the requesting user is authorized to access it.

Citations must not reference unauthorized, missing, or unrelated source content.

## 7. Retrieval Strategy

The system will:

1. Receive and validate the user query.
2. Determine the applicable access and document filters.
3. Search indexed content using vector and text retrieval.
4. Enforce metadata, version, and authorization restrictions.
5. Rank eligible results by relevance and source authority.
6. Return traceable chunks for grounded answer generation.

If sufficient authorized evidence cannot be found, the system must follow the safe abstention rules defined in `spec.md`.

## 8. References

- `spec.md` — RAG functional requirements and acceptance criteria.
- `document_metadata_model.md` — Document and chunk metadata schemas.
- `knowledge_base_inventory.csv` — Validated source inventory.
- `clarification-log.md` — Confirmed and open business decisions.

**Related specification:** BR-01, BR-02, BR-04, BR-06, BR-09, BR-10, AC-MET-05, AC-MET-06, and AC-RET-01 to AC-RET-07.