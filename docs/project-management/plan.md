# Implementation Plan: Banking Complaint Resolution Assistant

## Architecture Direction

The solution will follow a guided investigation workflow, progressively extended with a Controlled Investigation Agent during Sprint 3.

The system will:
1. Receive complaint information.
2. Validate required intake information.
3. Classify complaints and determine urgency.
4. Retrieve operational facts.
5. Retrieve approved policy guidance.
6. Build an evidence package.
7. Generate an evidence-based recommendation.
8. Route sensitive or escalated cases for human review.
9. Record authorized final decisions and audit information.

**Sprint 3 agent design:** The Controlled Investigation Agent will use hybrid dynamic orchestration. The language model may propose the next tool operation based on the user request and investigation state, but deterministic application and tool-boundary controls will validate permissions, inputs, business rules, and required human approvals before execution. Existing banking services and the Week 4 RAG pipeline must be reused, not rebuilt.

## Major Components

### Complaint Intake Component

**Role:**
- Receive complaint submissions.
- Validate mandatory fields.
- Create complaint records through an authorized intake workflow.
- Assign or request `Needs Information` handling when required information is missing, according to the existing complaint lifecycle.

**References:** Preconditions; Business Rules; Error Conditions.

### Classification Component

**Role:**
- Determine whether a submission is a complaint.
- Assign one or more complaint categories, as supported by the approved domain rules and data model.
- Calculate or propose an urgency level.
- Identify possible escalation requirements.
- Support justified reassessment when new evidence becomes available.

**References:** Complaint Definition; Business Rules; Domain Rules; Positive and Edge Scenarios.

### Evidence Retrieval Component

**Role:**
- Retrieve structured operational data through authorized services.
- Retrieve approved policy guidance using the existing RAG service.
- Preserve source references, access restrictions, and policy versions.
- Report missing, insufficient, or contradictory evidence.

**References:** Scope; Error Conditions; Reliability Constraints; Audit Constraints; Week 4 RAG interface.

### Recommendation Component

**Role:**
- Generate evidence-based complaint recommendations.
- Keep separate customer assertions, verified facts, policy evidence, and generated analysis.
- Include citations and limitations; abstain from unsupported policy conclusions.
- Propose rather than execute sensitive decisions.

**References:** Domain Rules; High-Level Interface Expectations.

### Human Review Component

**Role:**
- Route escalated or sensitive cases for analyst or supervisor review.
- Support requests for human approval and recording of authorized decisions.
- Enforce role-specific restrictions and mandatory human control over sensitive outcomes.

**References:** Core Flows; Domain Rules; Measurable Success Criteria; Approved Tool Catalogue.

### Audit Component

**Role:**
- Record complaint status changes, recommendations, tool activity, and reviewer actions.
- Maintain complaint and investigation history.
- Preserve the evidence and rationale associated with authorized decisions.

**References:** Audit Constraints; Non-Functional Requirements; Approved Tool Catalogue.

### Controlled Investigation Agent (Sprint 3 Extension)

**Role:**
- Interpret the requested investigation task and dynamically select from the approved tool catalogue.
- Maintain a bounded investigation context with completed steps, retrieved facts, policy evidence, unresolved issues, and pending human actions.
- Validate every proposed tool invocation through deterministic, role-aware tool boundaries.
- Combine returned results into a traceable evidence package and recommendation.
- Stop safely on missing authorization, missing evidence, tool failure, or execution limits.

**Design boundaries:**
- The LLM proposes tool calls; application and tool boundaries authorize and execute them.
- Do not bypass approved tools, business validation, access controls, or human approvals.
- Do not recreate database services, embeddings, vector storage, or RAG generation.
- The initial agent tool inventory is limited to the approved catalogue; capabilities not exposed there remain dependencies, not assumed MCP tools.

**References:** Sprint 1 Specification; Exercise 5.1.1; Approved Tool Catalogue and MCP Definitions; Failure Scenarios.

## Implementation Sequence

The implementation follows the project sprint roadmap. Each sprint consumes previously approved components rather than recreating them.

### Sprint 1 – Specification & Data Foundation

**Objectives:** Specification, working model of intake prompts, complaint domain rules, and structured-data foundation.

### Sprint 2 – Complaint API & RAG Service

**Objectives:** Tested complaint API and citation-enabled RAG knowledge service, available for reuse by the agent.

### Sprint 3 – Tools & Investigation Workflow

**Objectives:** Controlled MCP tools, a single Controlled Investigation Agent, a bounded investigation workflow, and human approval integration.

**Implementation approach:**

1. **Confirm the approved scope and dependencies.** Map Sprint 1 requirements to existing complaint/domain services, the Week 4 RAG interface, and the approved MCP catalogue. Track unresolved gaps and the pending Week 4 release approval.
2. **Define a tool catalogue and interfaces.** Map each approved tool to an existing service or a planned adapter; specify typed inputs/outputs, role restrictions, error outcomes, and audit evidence. Preserve the nine approved tool boundaries.
3. **Establish controlled tool execution.** Validate tool identity, arguments, caller authorization, case context, and business rules independently of the model. No model-generated role or confirmation is trusted.
4. **Build the investigation orchestration.** Allow dynamic selection of authorized operations for complaint/customer/account lookup, policy search, and case investigation. Record observations and enforce a maximum number of steps and termination conditions.
5. **Reuse RAG for policy-dependent operations.** Use the existing policy service, preserve citations, support status, and limitations, and withhold unsupported recommendations. Enforce authorization independently of retrieval access-label filters.
6. **Apply human-review boundaries.** Keep approval decisions human-only. Allow case notes, approval requests, status changes, and closure only through their specifically authorized tool flows and validations.
7. **Generate traceable outputs.** Build an evidence package containing verified facts, customer assertions, policy references, recommendations, limitations, and appropriate review route.
8. **Test and capture evidence.** Exercise normal, boundary, denied, and dependency-failure scenarios using synthetic data, then document defects and limitations.

**Approved tool inventory (T-001 to T-009):**

| ID | Tool | Intended use and boundary |
|---|---|---|
| T-001 | `get_customer` | Read-only synthetic customer lookup; Analyst or Supervisor |
| T-002 | `get_accounts` | Read-only account summaries for a verified customer; Analyst or Supervisor |
| T-003 | `get_complaint` | Read-only complaint details, status, and history; Analyst or Supervisor |
| T-004 | `search_policy` | Approved policy retrieval with applicable version and access restrictions; Analyst or Supervisor |
| T-005 | `create_case_note` | Add an authorized case note with evidence references and audit event |
| T-006 | `request_approval` | Analyst requests case-specific approval for a proposed action |
| T-007 | `record_approval_decision` | Human-only Supervisor decision and audit record |
| T-008 | `update_complaint_status` | Role-authorized status transition with validation and audit |
| T-009 | `close_complaint` | Sensitive Supervisor-only closure after evidence/approval checks |

**Scope gaps to track:** The approved catalogue does not define a complaint-creation tool, a dedicated classification/urgency tool, or a transaction-level evidence lookup tool. These remain requirements or interface gaps to clarify, not implicitly authorized agent actions. The agent may prepare recommendations about these operations, but shall not invent or execute unapproved tools.

**Safety and failure cases:** Handle SQL unavailability, vector-store unavailability, MCP timeouts, model rate limits, invalid transitions, rejected approvals, denied access, and missing or conflicting evidence. Fail safely without fabricated results or unauthorized changes.

**Sprint 3 handover:** Document agent behavior, tool boundaries, unresolved gaps, test evidence, and a reviewable pull request.

### Sprint 4 – Analyst Portal

**Objectives:** React analyst portal, deployment pipeline, monitoring, and runbooks.

### Sprint 5 – Quality, Security & Validation

**Objectives:** Evaluation, security, guardrails, resilience evidence, and production-readiness review.