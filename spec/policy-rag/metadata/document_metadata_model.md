# Complaint Policy RAG — Document Metadata Model

## 1. Overview

This document defines the metadata model for documents and chunks used by the Complaint Policy RAG Knowledge Service.

The model supports document identification, source traceability, version management, access-control filtering, and citation generation.

It is based on the requirements defined in `spec.md`, the FDM metadata model template, and the knowledge base retrieval guide.

## 2. Document Metadata Schema

Each document must have metadata describing its identity, classification, applicability, access restrictions, and source location.

### 2.1 Document-Level Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `source_id` | String | Yes | Unique document identifier |
| `title` | String | Yes | Document title |
| `document_type` | String | Yes | Policy, Guide, Matrix |
| `category` | String | Proposed | Business or subject category, distinct from document type |
| `version` | String | Yes | Document version |
| `effective_date` | Date | Yes | Date on which the document becomes active |
| `status` | String | Yes | Approved, Superseded |
| `access_label` | String | Yes | Access classification used for authorization filtering : Internal, Restricted |
| `checksum` | String | Proposed | Detect document changes |
| `relative_path` | String | Yes | Location of the original document within the knowledge base |

The mandatory status of `category` and `checksum` must be confirmed before ingestion.

### 2.2 Allowed Values and Formats

| Field | Validation Rule |
|---|---|
| `source_id` | Non-empty and unique |
| `title` | Non-empty string |
| `document_type` | Must match an approved document classification |
| `category` | Must belong to the validated business category list once approved |
| `version` | Non-empty string |
| `effective_date` | Valid date in `YYYY-MM-DD` format |
| `status` | Observed values: `Approved`, `Superseded` |
| `access_label` | Observed values: `Internal`, `Restricted` |
| `checksum` | Must be generated |
| `relative_path` | Non-empty relative path referencing an existing source file |

Observed values do not necessarily represent exhaustive allowed-value lists. Final validation rules must be confirmed against the approved specification.

### 2.3 Document Validation Rules

- Documents must contain all confirmed mandatory metadata fields.
- `source_id` must uniquely identify a source document within the inventory.
- Document versions must be stored as strings to preserve version identifiers.
- `effective_date` must represent a valid calendar date.
- Documents with missing or invalid access metadata must not become retrievable.
- Superseded documents must not be used as authoritative evidence for current-policy questions.
- Documents with inconsistent version and checksum information must be flagged for investigation.
- Invalid metadata must be reported and the affected document excluded from retrieval until corrected.

### 2.4 Metadata Enrichment

The original knowledge base manifest does not contain `category` or `checksum`.
The inventory contains proposed business categories that require confirmation.
The checksum generation method, mandatory status, and validation format must be defined before ingestion.
Metadata enrichment must preserve the original source identifiers, document versions, approval status, and access classifications.

### 2.5 Traceability

Every document must remain identifiable through its `source_id`.

Document metadata must support:
- Identification of the original source.
- Verification of the applicable document version.
- Access-control filtering.
- Association between retrieved chunks and their source documents.
- Citation generation using source and section information.

## 3. Chunk Metadata Schema

Each document chunk must preserve sufficient metadata to identify its source, maintain document structure, enforce access restrictions, and support accurate citation generation.

### 3.1 Chunk-Level Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `chunk_id` | String | Yes | Unique identifier for the chunk |
| `source_id` | String | Yes | Reference to the original source document |
| `section_name` | String | Yes | Document heading |
| `sequence` | Integer | Yes | Position of the chunk within the source document |
| `access_label` | String | Yes | Security label |

The `source_id` and `section_name` fields must allow each chunk to be traced to its original document and relevant section.

### 3.2 Validation Rules

- `chunk_id` must be unique within the indexed chunk collection.
- `source_id` must reference an existing document in the validated source inventory.
- `section_name` must identify the relevant source section or heading.
- `sequence` must be a non-negative integer and preserve the order of chunks within a document.
- `access_label` must contain an approved access classification.
- Chunk access restrictions must remain consistent with the source document's access requirements.
- Chunks with missing or invalid mandatory metadata must not be made available for retrieval.

### 3.3 Source Traceability

Every chunk must be traceable to exactly one source document through `source_id`.

### 3.4 Access Control Consistency

Chunk metadata must preserve the access restrictions applicable to the source document.

### 3.5 Citation Mapping

Each retrieved chunk must provide the metadata required to construct a traceable citation.

The citation mapping must associate:

- The retrieved `chunk_id`.
- The source document `source_id`.
- The relevant `section_name`.
- The corresponding document title and version.

The final citation representation must remain consistent with the approved RAG specification and grounded-answer response schema.

### 3.6 Example Chunk Metadata

The following example illustrates the proposed chunk metadata structure:

```json
{
  "chunk_id": "KB-001#s2#0001",
  "source_id": "KB-001",
  "section_name": "Complaint Investigation",
  "sequence": 1,
  "access_label": "Internal"
}
```

**Related requirements:** BR-02, BR-04, BR-08, BR-09, AC-MET-02, AC-MET-03, AC-MET-06, AC-RET-07.