# Approved Tool Catalogue

## 1. Purpose

This document defines the approved tools available to the Controlled Investigation Agent of the Banking Complaint Resolution Assistant.

The catalogue establishes the purpose, inputs, outputs, authorized roles, and operational controls of each tool.

It serves as the reference for tool schemas, error handling, MCP contracts, and subsequent tool implementation exercises.

Only tools explicitly included in the approved catalogue may be exposed to the agent.

## 2. Tool Design Principles

The following principles apply to all approved tools:

- Each tool must have one clearly defined and bounded purpose.
- Inputs and outputs must be typed and validated.
- Authorization must be enforced at the tool boundary, independently of the LLM.
- Sensitive operations must respect mandatory human approval requirements.
- Tool failures must return controlled errors without fabricating data.
- Every tool action must produce appropriate audit evidence.
- Existing banking services and the approved RAG implementation must be reused rather than duplicated.

## 3. Approved Tool Inventory

The Controlled Investigation Agent may use only the following nine approved tools. Each tool has a bounded responsibility and must enforce its authorization and validation controls independently of the LLM.

| ID | Tool Name | Operation | Allowed Roles | Specific Control |
|---|---|---|---|---|
| T-001 | `get_customer` | Read | Analyst, Supervisor | Read-only; BR-004/027 |
| T-002 | `get_accounts` | Read | Analyst, Supervisor | Read-only; field minimization |
| T-003 | `get_complaint` | Read | Analyst, Supervisor | Read-only |
| T-004 | `search_policy` | Read | Analyst, Supervisor | Current-version and access filters |
| T-005 | `create_case_note` | Write | Analyst, Supervisor | Parameterized inputs; no secrets; audit |
| T-006 | `request_approval` | Write | Analyst | Case-specific approval; BR-029 |
| T-007 | `record_approval_decision` | Write | Supervisor | Human-only decision |
| T-008 | `update_complaint_status` | Write | Authorized role | State-transition validation |
| T-009 | `close_complaint` | Write | Supervisor | Sensitive operation; BR-018/038 |

**Catalogue constraints:**

- Tool roles and permissions must be enforced by the application and MCP tool boundary.
- `record_approval_decision` requires an actual human Supervisor decision.
- `close_complaint` is reserved for authorized Supervisors and requires the applicable closure checks.
- `update_complaint_status` is permitted only when the caller is authorized and the requested transition is valid.
- Complaint creation, classification updates, urgency updates, and transaction-level retrieval are not approved as separate MCP tools in this catalogue.

## 4. Tool Definitions

### T-001 — get_customer

**Purpose**

Retrieve an existing synthetic customer record using its unique customer identifier.

**Input**

- `customer_id` (string, required): Identifier of the customer to retrieve.

**Output**

- Customer record when the identifier matches an existing customer.
- `not_found` when no matching customer exists.

**Dependencies**

- Existing customer data service or customer API.
- Existing role-based authorization mechanism.

**Error Handling**

- Invalid or missing `customer_id`: return a controlled validation error.
- Unauthorized caller: deny access without exposing customer information.
- Unknown `customer_id`: return `not_found` without inventing customer data.
- Unavailable customer data service: return a controlled service error.

---

### T-002 — get_accounts

**Purpose**

Retrieve account summaries associated with a verified synthetic customer.

**Input**

- `customer_id` (string, required): Identifier of the verified customer whose accounts must be retrieved.

**Output**

- A collection of account summaries associated with the customer.
- An empty collection when the verified customer has no associated accounts.

**Dependencies**

- Existing customer and account data services.
- Existing role-based authorization mechanism.
- Customer verification mechanism.

**Error Handling**

- Invalid or missing `customer_id`: return a controlled validation error.
- Unauthorized caller: deny access without exposing account information.
- Customer not found or not verified: do not return account information.
- Unavailable account data service: return a controlled service error.

---

### T-003 — get_complaint

**Purpose**

Retrieve an existing complaint record, including its details, current status, and available status history.

**Input**

- `complaint_id` (string, required): Identifier of the complaint to retrieve.

**Output**

- Complaint details, current status, and history when the complaint exists.
- `not_found` when no matching complaint exists.

**Dependencies**

- Existing Week 4 RAG retrieval service.
- Existing policy knowledge base and vector index.
- Document metadata and versioning strategy.
- Existing authorization mechanism.

**Error Handling**

- Invalid or missing `complaint_id`: return a controlled validation error.
- Unauthorized caller: deny access without disclosing complaint details.
- Unknown `complaint_id`: return `not_found`.
- Unavailable complaint service or database: return a controlled service error.

---

### T-004 — search_policy

**Purpose**

Retrieve relevant evidence from approved banking policies, procedures, and guidance documents to support complaint investigation.

**Input**

- `query` (string, required): Policy-related search query.
- `filters` (object, required): Applicable document metadata filters.
- `top_k` (integer, required): Maximum number of ranked evidence results requested.

**Output**

- Ranked policy evidence with associated document metadata.
- An empty evidence collection when no applicable results are available.

**Dependencies**

- Existing Week 4 RAG retrieval service.
- Existing policy knowledge base and vector index.
- Document metadata and versioning strategy.
- Existing authorization mechanism.

**Error Handling**

- Empty or invalid `query`: return a controlled validation error.
- Invalid filters or `top_k`: return a controlled validation error.
- Unauthorized access to restricted evidence: deny disclosure.
- No relevant approved evidence: return an empty result without fabricated citations.
- Unavailable retrieval service or vector store: return a controlled service error.

---

### T-005 — create_case_note

**Purpose**

Add an investigation note to an existing complaint, preserving supporting evidence references and creating an auditable record.

**Input**

- `complaint_id` (required): Identifier of the complaint.
- `note` (required): Investigation note content.
- `evidence_refs` (required): References to supporting evidence.

The exact data types and constraints for these fields shall be confirmed in `tool_schemas.json`.

**Output**

- Created note identifier.
- Associated audit event.

**Dependencies**

- Existing complaint and case-note persistence services, or an approved adapter.
- Existing audit mechanism.
- Existing authorization mechanism.

**Error Handling**

- Missing or invalid input: return a controlled validation error.
- Unauthorized caller: reject the operation.
- Unknown or inaccessible complaint: reject note creation.
- Unavailable persistence service: return a controlled service error.
- Failed write operation: do not report successful note creation.

---

### T-006 — request_approval

**Purpose**

Create a formal human approval request for a proposed action associated with an existing complaint.

**Input**

- `complaint_id` (required): Identifier of the relevant complaint.
- `action` (required): Proposed action requiring approval.
- `parameters` (required): Parameters associated with the proposed action.
- `evidence_refs` (required): Supporting evidence references.

The exact field types and allowed action values shall be defined in the tool schema and validated against existing business rules.

**Output**

- Approval request identifier.
- Approval request status.

**Dependencies**

- Existing complaint and approval workflow services, or an approved adapter.
- Existing business rules and authorization mechanism.
- Existing audit mechanism.

**Error Handling**

- Missing or invalid parameters: return a controlled validation error.
- Unauthorized caller: reject the request.
- Unknown or inaccessible complaint: reject the request.
- Unsupported proposed action: reject the request.
- Unavailable approval service: return a controlled service error.

---

### T-007 — record_approval_decision

**Purpose**

Record a human Supervisor's approval or rejection decision for an existing approval request.

**Input**

- `approval_id` (required): Identifier of the approval request.
- `decision` (required): Human approval or rejection decision.
- `reason` (required): Rationale supporting the decision.

The exact data types and accepted decision values shall be specified in `tool_schemas.json`.

**Output**

- Recorded approval decision.
- Associated audit event.

**Dependencies**

- Existing approval workflow service or approved adapter.
- Existing authenticated human Supervisor workflow.
- Existing audit mechanism.

**Error Handling**

- Invalid or missing input: return a controlled validation error.
- Unauthorized caller or absent authenticated human decision: reject the operation.
- Unknown approval request: return a controlled not-found error.
- Invalid approval state or decision: reject the operation.
- Unavailable approval service: return a controlled service error.

---

### T-008 — update_complaint_status

**Purpose**

Apply an authorized and valid status transition to an existing complaint.

**Input**

- `complaint_id` (required): Identifier of the complaint.
- `target_status` (required): Requested destination status.
- `reason` (required): Justification for the transition.

The exact types and permitted status values shall follow the existing complaint domain model.

**Output**

- Updated complaint status.
- Associated audit event.

**Dependencies**

- Existing complaint domain model and status-transition rules.
- Existing complaint persistence service.
- Existing authorization and audit mechanisms.

**Error Handling**

- Missing or invalid parameters: return a controlled validation error.
- Unauthorized caller: reject the transition.
- Unknown complaint: return a controlled not-found error.
- Invalid state transition: reject without changing the complaint status.
- Required approval missing or rejected: do not apply the transition.
- Unavailable complaint service: return a controlled service error.

---

### T-009 — close_complaint

**Purpose**

Close an existing complaint after the required evidence and approval conditions have been validated.

**Input**

- `complaint_id` (required): Identifier of the complaint to close.
- `resolution` (required): Recorded complaint resolution.
- `communication_date` (required): Relevant communication date.
- `evidence_refs` (required): Supporting evidence references.

The exact field types, date format, and validation constraints shall be defined in `tool_schemas.json`.

**Output**

- Closed complaint record or closure confirmation.
- Associated audit event.

**Dependencies**

- Existing complaint lifecycle and closure rules.
- Existing approval workflow.
- Existing complaint persistence service or approved adapter.
- Existing authorization and audit mechanisms.

**Error Handling**

- Missing or invalid parameters: return a controlled validation error.
- Unauthorized caller: reject closure.
- Unknown complaint: return a controlled not-found error.
- Insufficient evidence or missing required approval: reject closure.
- Invalid complaint state: reject closure without modifying the record.
- Unavailable complaint service: return a controlled service error.

---

**Schema and error handling note**

Exact request and response structures, error codes, validation constraints, and any required execution-context fields shall be defined in `tool_schemas.json` and `tool_error_matrix.csv`.