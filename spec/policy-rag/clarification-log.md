# Complaint Policy RAG — Clarification Log

## 1. Purpose

This document records requirement clarifications, confirmed decisions, and unresolved questions for the Complaint Policy RAG Knowledge Service.

It ensures that business rules, retrieval behavior, metadata requirements, and access restrictions are understood before implementation.

## 2. Clarification Register

### CL-001 — Approved Documents

**Question:** Which documents are approved?

**Findings:**
The `knowledge_base_manifest.csv` identifies 13 documents:
- 12 documents with status `Approved`.
- 1 document (`KB-001-OLD`) with status `Superseded`.

The `corpus_inventory.json` additionally lists `KB-GUIDE` as an approved training document.

Approved documents include policies, operational playbooks, guides, FAQ articles, historical casebooks, and bulletins.

**Confirmed rules:**
- Current approved policies and playbooks are authoritative within their applicable scope.
- Bulletins clarify policies unless explicitly stated otherwise.
- FAQs provide supporting information but do not override authoritative policies.
- Historical casebooks are illustrative and are not binding precedents.
- Superseded sources are historical only.
- Retrieval must respect document status, applicability, and access restrictions.

**Status:** Resolved.
**Sources:**
- `corpus_inventory.json`
- `knowledge_base_manifest.csv`
- `Knowledge_Base_Content_Map_and_Retrieval_Guide.docx`, Sections 1–2.
**Related Spec:** BR-01, BR-06, BR-10, AC-RET-01.

---

### CL-002 — Mandatory Metadata

**Question:** Which metadata is mandatory?
**Findings:**

The retrieval guide identifies the following required metadata:
- `source_id`
- `title`
- `version`
- `effective_date`
- `status`
- `access_label`
- `section_title`
- `chunk_id`

The metadata model template additionally defines:
- `document_type`
- `category`
- `checksum`
- `sequence`
- Document-to-chunk source mapping.

**Confirmed requirements:**
- Metadata must support source identification, applicability, access filtering, and citation traceability.
- Each chunk must be traceable to its source document.
- Retrieval filtering must support `document_type`, effective version, and `access_label`.
**Remaining questions:**
- Which additional template fields are mandatory at ingestion?
- What are the permitted values and validation formats?
- How should missing `category` and `checksum` values be populated?
- Which fields must be stored at document level versus chunk level?
**Status:** Partially Resolved.
**Sources:**
- `metadata_model_template.md`
- `knowledge_base_manifest.csv`
- `Knowledge_Base_Content_Map_and_Retrieval_Guide.docx`, Section 3.
**Related Spec:** BR-08, BR-09, AC-MET-01 to AC-MET-06.

---

### CL-003 — Valid Citations

**Question:** What forms a valid citation?
**Findings:**

The retrieval guide identifies `source_id`, `title`, `section_title`, and `chunk_id` as metadata supporting source identification and citation traceability.

The grounded-answer schema requires a `citations` array in every response.

**Confirmed requirements:**
- Grounded answers must include supporting citations.
- Citations must be traceable to their source documents and relevant passages.
- The cited evidence must be authorized and applicable to the requesting user.
- Citations must not rely on superseded policies as current authority.

**Remaining questions:**
- What is the exact citation object structure?
- Must every citation include document version and effective date?
- Should citations contain direct links or passage identifiers?
- What additional citation validation requirements are defined by the RAG citation-control bulletin?

**Status:** Partially Resolved.
**Sources:**
- `grounded_answer_schema.json`
- `metadata_model_template.md`
- `Knowledge_Base_Content_Map_and_Retrieval_Guide.docx`, Section 3.
**Related Spec:** BR-04, AC-CIT-01 to AC-CIT-05.

---

### CL-004 — Insufficient Evidence

**Question:** What should happen when evidence is insufficient?
**Confirmed decision:**

The system must safely abstain when supporting evidence is missing, insufficient, conflicting, or outside the approved scope.
The system must not generate unsupported policy instructions using the LLM's general knowledge.
The approved guidance also requires unsupported or conflicting cases to be routed to an authorized human reviewer.

**Response expectations:**
- `supported` must be `false`.
- `answer` must clearly communicate the inability to provide a supported answer.
- `citations` must not contain fabricated references.
- `limitations` must describe the reason for the limitation.

**Status:** Resolved — Core behavior confirmed.
**Sources:**
- Exercise 4.1.1 specification.
- `grounded_answer_schema.json`
- `Knowledge_Base_Content_Map_and_Retrieval_Guide.docx`, Training Notice and Section 2.
**Related Spec:** BR-05, AC-ABS-01 to AC-ABS-05.

---

### CL-005 — Role-Based Access

**Question:** Which access labels may each role retrieve?
**Findings:**
The current manifests contain two access labels:
- `Internal`
- `Restricted`

The metadata template requires retrieval filtering using `access_label`.

**Confirmed requirements:**
- Retrieval must enforce applicable access restrictions.
- Unauthorized documents must not be provided to the answer-generation component or exposed through citations.
- Document relevance or similarity must not override access-control restrictions.
**Remaining questions:**
- Which roles may access `Internal` documents?
- Which roles may access `Restricted` documents?
- Is the authorization model hierarchical or based on explicit permissions?
- How will authenticated requester permissions be supplied to the RAG service?

**Status:** Open — Role-to-access-label mapping not confirmed.
**Sources:**
- `corpus_inventory.json`
- `knowledge_base_manifest.csv`
- `metadata_model_template.md`
**Related Spec:** BR-02, AC-RET-02.

---

### CL-006 — Superseded Versions

**Question:** How are superseded versions handled?

**Confirmed decision:**
Superseded documents must be treated as historical sources and must not be used as authoritative evidence for current-policy questions.
The corpus identifies `KB-001-OLD`, version 1.4, as `Superseded`.
The currently approved `KB-001`, version 3.0, is the authoritative complaint management policy within its applicable scope.

**Additional consideration:**
Historical retrieval may require a separately authorized use case. The exact rules for such retrieval have not yet been specified.

**Status:** Resolved for current-policy queries; historical retrieval permissions remain open.
**Sources:**
- `corpus_inventory.json`
- `knowledge_base_manifest.csv`
- `Knowledge_Base_Content_Map_and_Retrieval_Guide.docx`, Section 2.
**Related Spec:** BR-06, BR-10, AC-RET-04.

---

### CL-007 — Conflicting Approved Policies

**Question:** How should the system behave when current authoritative sources contain contradictory instructions?
**Confirmed decision:**
The system must abstain from presenting conflicting policy instructions as a supported answer.
The conflict must be routed to the relevant policy owner or authorized human reviewer.
The system must not arbitrarily select a source based only on similarity score, publication date, or LLM preference.
**Status:** Resolved.
**Source:** `Knowledge_Base_Content_Map_and_Retrieval_Guide.docx`, Section 2.
**Related Spec:** BR-03, BR-05, BR-06, BR-10, AC-ABS-03.

---

### CL-008 — Retrieval Evaluation Thresholds

**Question:** What measurable retrieval quality thresholds must the RAG service achieve?
**Findings:**

The exercise requires measurable retrieval evidence.

The retrieval guide identifies evaluation scenarios covering exact-title lookup, natural-language queries, overlapping sources, section-specific retrieval, access restrictions, superseded documents, and unsupported questions.
**Remaining questions:**
- Which evaluation metrics should be used (for example, Recall@K or Precision@K)?
- What values of K are required?
- What minimum quality thresholds must be achieved?
- Which evaluation dataset will be used?
**Status:** Open — Awaiting evaluation requirements.
**Sources:**
- Exercise 4.1.1 specification.
- `Knowledge_Base_Content_Map_and_Retrieval_Guide.docx`, Section 4.
**Related Spec:** AC-RET-05, NFR-01.

## 3. Open Decisions Summary

| ID | Outstanding decision |
|---|---|
| CL-002 | Confirm mandatory metadata fields, formats, and enrichment rules. |
| CL-003 | Confirm the exact citation structure and validation rules. |
| CL-005 | Define role-to-access-label permissions. |
| CL-006 | Clarify authorization for historical queries, if supported. |
| CL-008 | Define retrieval evaluation metrics and thresholds. |
