# Complaint Policy RAG — Specification

Exercise: 4.1.1 — Author the Complaint Policy RAG Specification
Status: Draft — pending source-manifest and coach validation
Reference templates: metadata_model_template.md, grounded_answer_schema.json

## 1. Overview

The Complaint Policy RAG Knowledge Service assists complaint analysts by answering questions about banking complaint policies, procedures, and escalation guidance using approved, applicable, and authorized source material. Answers must be grounded in retrieved evidence and traceable to their sources. When evidence is insufficient, the service must safely abstain.

## 2. Scope and Non-goals

### 2.1 In Scope

The Complaint Policy RAG Knowledge Service must:

- Answer questions related to banking complaint policies, procedures, and escalation guidelines.
- Retrieve applicable approved content that the requester is authorized to access.
- Generate evidence-grounded answers and provide traceable citations.
- Abstain from answering when sufficient supporting evidence cannot be found or conflicting evidence cannot be resolved under approved rules.
- Expose a documented interface to authorized applications.

### 2.2 Non-goals

The Complaint Policy RAG Knowledge Service must not:

- Approve or execute financial transactions, refunds, or account modifications.
- Create, modify, or override existing banking policies.
- Provide unsupported answers based solely on the LLM's general knowledge.
- Reveal documents or metadata outside the requester's authorized access.
- Replace authorized human decisions; provide independent legal or financial advice.

## 3. Actors

### 3.1 Complaint Analyst
Requests approved procedural guidance for handling complaints.

### 3.2 Team Lead
The Team Lead uses the service to review complaint-handling procedures and support analysts in complex cases.

### 3.3 Backend Service
Submits requests through the RAG service API and receives structured responses.

## 4. Preconditions

Before processing a user query, the following conditions must be satisfied:

- The knowledge base must contain validated and approved policy documents.
- Policy metadata permits filtering by document_type, applicable version/effective date, and access_label.
- Approved documents must be processed, indexed, and available for retrieval.
- The requesting user or system must be authenticated and authorized to access the relevant policy documents.
- The retrieval and answer-generation components must be operational.

If these preconditions are not met, the system must not generate an unsupported answer. It must return an appropriate error or abstention response depending on the situation.

## 5. Main Flow

### 5.1 Successful Query Flow

1. The Complaint Policy RAG Knowledge Service receives and validate the request and its authorized requester context.
2. Apply approved document eligibility and access filters before exposing evidence.
3. Retrieve potentially relevant document chunks and their source metadata.
4. The system evaluates whether the retrieved evidence is sufficient to answer the user's question.
5. If sufficient evidence is available, the system generates an answer grounded exclusively in the retrieved information.
6. Return the answer, support indicator, citations, and limitations using the grounded-answer response contract in Section 9.

### 5.2 Alternative Flow — Insufficient Evidence

1. The system receives and validates the query.
2. The system attempts to retrieve relevant information from approved and authorized policy documents.
3. If the retrieved evidence is insufficient to support an answer, the system must abstain from generating unsupported claims.
4. Return a clear abstention message, supported: false, and no fabricated citations.
5. Record any material limitations in limitations, following the finalized schema rules.

### 5.3 Conflicting Evidence
If two applicable approved sources contradict each other and no authorized precedence rule resolves the conflict, the proposed safe behavior is to abstain and flag the conflict for review. This rule is pending confirmation (CL-007).

## 6. Business Rules

### BR-01 — Approved and Applicable Sources

The system must retrieve and use only approved policy documents that are applicable to the user's request.

Archived, outdated, unapproved, or unauthorized documents must not be used to generate answers unless explicitly permitted by an approved business rule.

### BR-02 — Access Control

Retrieval, response content, and citations must respect access_label and the requester's permissions. Exact allowed labels and role mappings require confirmation (CL-005).

### BR-03 — Grounded Answers

Every substantive policy claim in a supported answer must be justified by retrieved, authorized evidence. General model knowledge is not policy evidence.

### BR-04 — Source Citations

Supported answers must provide citations traceable to source content. Each chunk must map to its source through source_id and a section/heading locator. The final citation object and locator requirements remain open (CL-003).

### BR-05 — Safe Abstention

When evidence is insufficient, the service must not invent guidance. It must return supported: false and explain the limitation. Exact abstention text and citation-array policy require validation (CL-004).

### BR-06 — Policy Version Consistency

Retrieval must distinguish effective versions and avoid silently combining superseded and current-policy instructions. Rules for superseded documents and historical questions remain open (CL-006).

## BR-07 — Read-Only Assistance

The RAG service provides information only; it does not execute banking actions or make final complaint decisions.

## BR-08 — Document and Chunk Metadata Contract

The metadata model must cover the following fields, preserving these names:

Document fields
- source_id: stable document identifier.
- document_type: classification used by the retrieval filter; this exact name is required.
- category: business/subject category, distinct from document_type.
- version: document version.
- effective_date: date from which a version is applicable.
- access_label: value used for access-controlled retrieval.
- checksum: source-content integrity value.


Chunk fields
- chunk_id: chunk identifier.
- source_id: link to the source document.
- heading/section: locator in the original source (final storage/API key to be decided).
- sequence: ordering of the chunk in its source.
- access_label: access-control value for the chunk.

The approved model must define requiredness, allowed values, formats, and cross-field consistency checks, including chunk-to-source mappings and access-label consistency. The supplied template does not specify these details; see CL-002.

## BR-09 — Retrieval Filters and Citation Mapping
Retrieval must support filtering by document_type, effective/applicable version, and access_label using the metadata model field names. Each retrieved chunk must remain traceable to source_id and its source section for citation creation.

## BR-10 — Source Authority Hierarchy

The RAG Knowledge Service must respect the authority hierarchy defined by the approved knowledge base guidance.
Current approved policies and playbooks are authoritative within their applicable scope.
Operational bulletins clarify referenced policies and must not override them unless explicitly stated.
FAQ documents provide supporting explanations but must not override authoritative policies.
Historical casebooks are illustrative and must not be treated as binding precedents.
Superseded documents must not be used as authoritative evidence for current-policy answers.
When current authoritative sources provide conflicting instructions, the system must abstain and route the conflict to the relevant policy owner.


## 7. Error Handling

The Complaint Policy RAG Knowledge Service must handle errors safely and consistently without generating unsupported information or exposing sensitive system details.

### 7.1 Insufficient Evidence

Return a safe abstention rather than an unsupported policy answer. This is distinct from a technical failure.

### 7.2 Unauthorized Access

Reject unauthorized requests without disclosing restricted source content or its protected metadata.

### 7.3 Retrieval Service Unavailable

Return a technical failure; never bypass retrieval and answer using unaudited model knowledge.

### 7.4 Answer Generation Failure

Return a technical failure, not an incomplete or unverified generated answer.

### 7.5 Invalid Query

Reject missing, empty, or malformed questions with an understandable validation error.

### 7.6 Error Response Requirements

Failure responses must distinguish validation, authentication/authorization, retrieval, and generation failures without exposing sensitive internals. The precise error body and HTTP codes remain to be agreed (CL-008).

## 8. Non-Functional Requirements (NFRs)

### NFR-01 — Performance

Establish a measurable response-time target, percentile, and workload after stakeholder confirmation (CL-009).

### NFR-02 — Security

Protect policy content, query data, and metadata according to applicable organizational security rules. Avoid sensitive data leakage through answers, citations, logs, and errors.

### NFR-03 — Reliability

Failures must produce predictable safe outcomes; neither dependency failure nor missing evidence may produce fabricated policy guidance.

### NFR-04 — Availability

Define the required availability target and measurement period with stakeholders (CL-009).

### NFR-05 — Observability and Traceability

Support operational diagnostics, auditability, and traceability without exposing restricted information.

### NFR-06 — Maintainability

Support authorized policy updates while preserving version-aware retrieval and citation traceability.


## 9. API Expectations

### 9.1 API Purpose

An authorized calling application must be able to submit a policy question. Requests must be validated and linked to an authorization context. Endpoint, authentication mechanism, and exact input format remain to be confirmed (CL-008).

### 9.2 Grounded Answer Response Contract
The provided `grounded_answer_schema.json` requires these **four fields** in a response object:

| Field | Type | Meaning |
|---|---|---|
| `answer` | string | Answer or abstention message |
| `supported` | boolean | Whether the answer is supported by evidence |
| `citations` | array | Supporting source references; item shape not defined by supplied template |
| `limitations` | array | Stated answer limitations; item shape not defined by supplied template |

No `status` field is required by the supplied schema. Do not treat a `status` field as part of the approved contract unless separately agreed.

**Illustrative supported response (citation object not yet finalized):**

```json
{
  "answer": "Follow the applicable dispute procedure.",
  "supported": true,
  "citations": [
    {"source_id": "EXAMPLE-POL-001", "version": "2.1", "section": "3.4"}
  ],
  "limitations": []
}
```

**Illustrative abstention response:**

```json
{
  "answer": "I could not find sufficient evidence in approved policy documents.",
  "supported": false,
  "citations": [],
  "limitations": ["Insufficient approved supporting evidence"]
}
```

Both examples are illustrative, not actual policy content or fully agreed API schemas. Citation and limitation item types, support criteria, and exact messages require confirmation (CL-003, CL-004, CL-008).

### 9.3 Citations and Metadata
Citation generation must use the document/chunk metadata mapping in BR-08 and BR-09, including the stable `source_id` and source locator. Retrieved metadata must not disclose unauthorized sources.

### 9.4 Errors
Client and dependency failures must be distinguishable from an ordinary `supported: false` response. Error envelope and HTTP status mappings remain open (CL-008).


## 10. Acceptance Criteria

### 10.1 Citation Requirements

**AC-CIT-01 — Citation Presence**

Given a valid question supported by approved and authorized policy documents,

When the system generates a grounded answer,

Then:
- The response must set `supported` to `true`.
- The `citations` array must contain at least one citation.

**AC-CIT-02 — Citation Traceability**

Given a grounded answer containing citations,

When the citations are validated,

Then:
- Each citation must reference an existing source document.
- Each citation must be traceable to a retrieved chunk and its source document through `chunk_id` and `source_id`.
- Each citation must identify the relevant source section or heading.

**AC-CIT-03 — Citation Authorization**

Given a user with restricted access permissions,

When the system generates a grounded answer,

Then:
- Every cited document must be approved and accessible to the requesting user.
- No citation may expose information from an unauthorized document.

**AC-CIT-04 — Citation Accuracy**

Given an answer containing one or more factual claims about a banking policy,

When the answer is evaluated against the cited source passages,

Then:
- Every policy-specific claim must be supported by at least one cited passage.
- Citations must not reference unrelated or contradictory evidence.

**AC-CIT-05 — Citation Response Structure**

Given a successfully processed query,

When the system returns a response,

Then:
- The response must contain `answer`, `supported`, `citations`, and `limitations`.
- `answer` must be a string.
- `supported` must be a boolean.
- `citations` must be an array.
- `limitations` must be an array.

## 10. Acceptance Criteria

### 10.1 Citation Requirements

**AC-CIT-01 — Citation Presence**

Given a valid question supported by approved and authorized policy documents,

When the system generates a grounded answer,

Then:
- The response must set `supported` to `true`.
- The `citations` array must contain at least one citation.

**AC-CIT-02 — Citation Traceability**

Given a grounded answer containing citations,

When the citations are validated,

Then:
- Each citation must reference an existing source document.
- Each citation must be traceable to a retrieved chunk and its source document through `chunk_id` and `source_id`.
- Each citation must identify the relevant source section or heading.

**AC-CIT-03 — Citation Authorization**

Given a user with restricted access permissions,

When the system generates a grounded answer,

Then:
- Every cited document must be approved and accessible to the requesting user.
- No citation may expose information from an unauthorized document.

**AC-CIT-04 — Citation Accuracy**

Given an answer containing one or more factual claims about a banking policy,

When the answer is evaluated against the cited source passages,

Then:
- Every policy-specific claim must be supported by at least one cited passage.
- Citations must not reference unrelated or contradictory evidence.

**AC-CIT-05 — Citation Response Structure**

Given a successfully processed query,

When the system returns a response,

Then:
- The response must contain `answer`, `supported`, `citations`, and `limitations`.
- `answer` must be a string.
- `supported` must be a boolean.
- `citations` must be an array.
- `limitations` must be an array.

### 10.2 Abstention Requirements

**AC-ABS-01 — Insufficient Evidence**

Given a valid user query for which no sufficient supporting evidence exists in approved and authorized policy documents,

When the system processes the query,

Then:
- The system must abstain from generating unsupported policy information.
- The response must set `supported` to `false`.
- The `answer` field must contain a clear abstention message.
- The `citations` array must be empty when no supporting evidence was found.
- The `limitations` array must indicate that sufficient evidence was unavailable.

**AC-ABS-02 — Unsupported Questions**

Given a question outside the scope of the approved policy knowledge base,

When the system cannot retrieve sufficient relevant evidence,

Then:
- The system must not generate an answer based solely on the LLM's general knowledge.
- The response must set `supported` to `false`.
- The system must clearly indicate that the question cannot be answered using the available approved evidence.

**AC-ABS-03 — Conflicting Evidence**

Given two approved and applicable policy documents containing contradictory instructions,

When the system cannot resolve the conflict using confirmed business rules,

Then:
- The system must not arbitrarily select or combine contradictory instructions.
- The response must set `supported` to `false`.
- The system should identify the conflict as a limitation and flag it for review.

**Status:** Confirmed by Knowledge Base Retrieval Guide, Section 2.

**AC-ABS-04 — Abstention Response Structure**

Given a query resulting in safe abstention,

When the system returns its response,

Then:
- `answer` must be a string containing a clear abstention message.
- `supported` must be `false`.
- `citations` must be an array.
- `limitations` must be an array describing the relevant limitations.
- The response must conform to `grounded_answer_schema.json`.

**AC-ABS-05 — Retrieval Failure Is Not Abstention**

Given an unavailable retrieval service or inaccessible policy knowledge base,

When the system attempts to process a query,

Then:
- The system must return an appropriate technical error.
- The system must not treat the technical failure as evidence that no relevant policy exists.
- The system must not generate an unsupported answer as a fallback.

**Related requirements:** BR-03, BR-05, BR-06, Section 5.2, Section 7, Section 9.

### 10.3 Metadata Requirements

**AC-MET-01 — Document Metadata Completeness**

Given a policy document submitted for ingestion,

When the system validates its metadata,

Then:
- The document must contain all fields required by the approved metadata model.
- The system must validate metadata values against the confirmed formats and allowed values.
- Documents with missing or invalid mandatory metadata must be excluded from retrieval until corrected.
- Metadata enrichment requirements must be defined before ingestion.

**Pending clarification:** CL-002 — Mandatory Metadata.

**AC-MET-02 — Chunk Metadata Completeness**

Given an approved policy document divided into chunks,

When the system prepares the chunks for retrieval,

Then:
- Each chunk must contain a unique `chunk_id`.
- Each chunk must reference its source document through `source_id`.
- Each chunk must preserve its section or heading, sequence, and `access_label`.
- Chunks with invalid or incomplete required metadata must not be made available for retrieval.

**AC-MET-03 — Metadata Consistency**

Given a document and its associated chunks,

When their metadata is validated,

Then:
- Each chunk's `source_id` must reference an existing source document.
- Each chunk's access classification must be consistent with the applicable document access policy.
- Document versions and effective dates must allow the system to identify the applicable policy version.
- Inconsistent metadata must prevent affected content from becoming retrievable until resolved.

**AC-MET-04 — Metadata Validation**

Given a document or chunk with metadata,

When validation is performed,

Then:
- Required fields must be present.
- Field values must respect the approved formats and allowed values.
- Invalid or inconsistent metadata must be reported through a validation result.
- The system must not silently assign permissive access labels to missing or invalid access metadata.

**AC-MET-05 — Metadata-Based Retrieval Filtering**

Given a query submitted by an authorized requester,

When the system retrieves policy content,

Then:
- Retrieval must support filtering by `document_type`.
- Retrieval must respect the applicable document version and `effective_date`.
- Retrieval must enforce restrictions based on `access_label`.
- Only documents and chunks satisfying the applicable filters may be returned.

**AC-MET-06 — Citation Source Mapping**

Given a retrieved chunk used as evidence for an answer,

When the system constructs a citation,

Then:
- The citation must be traceable to the retrieved `chunk_id`.
- The chunk must reference a valid `source_id`.
- The source section or heading must be identifiable.
- The citation must not reference missing or unauthorized source content.

**Related requirements:** BR-01, BR-02, BR-04, BR-06, BR-08, BR-09, Section 9.

### 10.4 Retrieval Requirements

**AC-RET-01 — Approved Document Retrieval**

Given a valid query submitted by an authorized requester,

When the system retrieves relevant policy information,

Then:
- Only approved and applicable policy documents must be eligible for retrieval.
- Unapproved or superseded documents must be excluded unless explicitly permitted by confirmed business rules.
- Retrieved documents must satisfy the applicable metadata filters.

**AC-RET-02 — Role-Based Access Filtering**

Given a requester with defined access permissions,

When the system performs document retrieval,

Then:
- Only documents with an `access_label` permitted for that requester may be returned.
- Unauthorized documents and chunks must not be included in the evidence provided for answer generation.
- Similarity scores must not override access-control restrictions.

**AC-RET-03 — Document Type Filtering**

Given a query requiring a specific document classification,

When the system searches the knowledge base,

Then:
- Retrieval must support filtering using the exact `document_type` metadata field.
- Documents that do not satisfy the requested and authorized document-type filter must be excluded.

**AC-RET-04 — Effective Version Filtering**

Given multiple versions of the same policy document,

When the system retrieves information for a current-policy question,

Then:
- Only the approved version applicable to the question's effective date must be eligible.
- Superseded versions must not be used unless historical retrieval is explicitly authorized.
- The system must not combine incompatible policy versions into an unsupported answer.

**AC-RET-05 — Retrieval Relevance**

Given a valid question with relevant information available in approved and authorized documents,

When the system performs retrieval,

Then:
- The system must return relevant evidence suitable for grounded answer generation.
- Retrieved evidence must be traceable to its source documents.
- Retrieval quality must be evaluated against an agreed test dataset and measurable relevance criteria.
- The retrieval system must achieve Recall@5 ≥ 0.85 on the approved evaluation dataset.

**Status:** Retrieval quality targets and evaluation metrics require confirmation.

**AC-RET-06 — No Eligible Evidence**

Given a query for which no approved, applicable, and authorized supporting evidence is available,

When retrieval completes successfully,

Then:
- The system must not use unauthorized or unapproved documents as fallback evidence.
- The system must follow the safe abstention requirements defined in Section 10.2.
- The response must set `supported` to `false`.

**AC-RET-07 — Retrieval Traceability**

Given a set of retrieved policy chunks,

When the system prepares evidence for answer generation,

Then:
- Each chunk must have a valid `chunk_id` and `source_id`.
- Each chunk must be traceable to the relevant document section or heading.
- The system must preserve the metadata necessary for citation generation and access validation.
- Top 3 relevant document chunks must be returned. 

**Related requirements:** BR-01, BR-02, BR-03, BR-05, BR-06, BR-08, BR-09, Sections 5, 9, 10.2, and 10.3.