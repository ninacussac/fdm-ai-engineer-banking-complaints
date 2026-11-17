# Tasks: Banking Complaint Resolution Assistant

## Sprint 1 – Specification & Data Foundation

- [ ] T001 Finalize the complaint-resolution specification : Overview, scope, non-goals, actors, core flows, error conditions, NFRs, in-output expectation, BR, Domain Rules, Precondition, Positive/Negative/Edge scenarios, Measurable Success Criteria, Reliability constraints,  Security constraint, Privacy constraints and Audit constraints in the spec.md file.

- [ ] T002 Record all identified ambiguities, open questions, decisions, owners, and statuses in the clarification-log.md file.

- [ ] T003 Define complaint taxonomy : Define supported complaint categories and classification rules 

- [ ] T004 Create structured data model by defining Customer, Account, Complaint, Service Request, Status History, and Audit entities.

## Sprint 2 – Complaint API & RAG

- [ ] T005 Implement complaint intake API which supports complaint submission and validation.

- [ ] T006 Implement complaint classification service which determines whether a submission qualifies as a complaint and assign categories.

- [ ] T007 Calculate urgency and store the triggered rule.

- [ ] T008 Retrieve customer, account, complaint, and transaction information.

- [ ] T009 Implement RAG knowledge service : Retrieve approved procedures, policies, and escalation guidance with citations.

- [ ] T010 Ensure every retrieved policy statement includes source references.

## Sprint 3 – Workflow & Human Review

- [ ] T011 Build evidence package workflow : Combine customer assertions, verified facts, policy evidence, and generated analysis.

- [ ] T012 Implement recommendation generation. 

- [ ] T013 Implement escalation workflow : Route high-priority and sensitive cases to appropriate reviewers.

- [ ] T014 Implement supervisor review workflow : Support approve, reject, escalate, and request-changes actions.

- [ ] T015 Implement audit event recording : Record decisions, rationale, timestamps, and reviewer information.

### Sprint 3 — Controlled Investigation Agent & MCP Tasks

#### Specify the Controlled Investigation Agent

- [ ] **T026 — Align the agent scope and document dependencies.** Map the Sprint 1 complaint workflow and acceptance criteria to the existing components and approved tool catalogue and identify gaps (complaint creation, multi-category persistence, transaction lookup, classification/urgency interfaces). **Evidence:** `spec/agent/spec.md` and requirement notes.
- [ ] **T027 — Define the controlled agent behavior and boundaries.** Specify hybrid dynamic tool selection, mandatory tool-side authorization, human-only approval decisions, auditability, RAG abstention, bounded execution, and safe stops; distinguish recommendations from authorized operations. **Evidence:** `spec/agent/spec.md`.
- [ ] **T028 — Update the implementation plan and executable tasks.** Integrate the agent into the existing project `plan.md` and `tasks.md`; link each planned capability to its exercise, dependency, and test evidence. **Evidence:** reviewed `plan.md` and `tasks.md`.

#### Tool Catalogue

- [ ] **T029 — Map the nine approved tools to services and roles.** Document T-001 `get_customer`, T-002 `get_accounts`, T-003 `get_complaint`, T-004 `search_policy`, T-005 `create_case_note`, T-006 `request_approval`, T-007 `record_approval_decision`, T-008 `update_complaint_status`, and T-009 `close_complaint`, including purpose, typed I/O, authorization, errors, audit, and service owner. Do not assume `create_complaint` is approved. **Evidence:** tool catalogue and gap log.

#### Lookup Tools & Investigation Agent

- [ ] **T030 — Implement and verify approved read-only lookup adapters.** Reuse customer, account, complaint, and policy services for T-001–T-004. Apply authorization, field minimization, approved document filters, typed validation, and controlled not-found/error responses. Do not rebuild the RAG. **Evidence:** lookup integration tests.
- [ ] **T031 — Implement bounded dynamic investigation orchestration.** Select only approved operations, validate tool arguments and caller role independently of the LLM, maintain minimal investigation state and execution traces, enforce tool-call limits, and produce an evidence-based recommendation or safe abstention. **Evidence:** working agent plus normal, boundary, and failure tests.

#### MCP Contracts & Server

- [ ] **T032 — Define the approved MCP tool contracts.** Specify typed requests/responses, authorization context, errors, audit events, and idempotency/confirmation requirements where appropriate. Reconcile approved catalogue, mock API contracts, OpenAPI examples, and existing service behavior. **Evidence:** reviewable MCP contracts.
- [ ] **T033 — Expose approved service adapters through an MCP server.** Implement the validated contracts without duplicating domain, database, or RAG logic; reject unknown tools, invalid arguments, or unauthorized calls. **Evidence:** running MCP server and contract tests.

#### Least Privilege & Human Approval

- [ ] **T034 — Enforce least privilege and data minimization.** Validate the authenticated role and case-level permissions at every tool boundary, not from LLM-provided claims. Test denied customer/account/policy access and sensitive-data redaction. **Evidence:** role-authorization tests and audit events.
- [ ] **T035 — Implement controlled actions and human approval boundaries.** Integrate T-005–T-009 subject to approved roles and state-transition rules. T-007 is Supervisor human-only; T-009 is sensitive Supervisor-only. The agent must not autonomously approve or close complaints. Status transitions may only be executed through T-008 when the requesting user is authorized and all applicable business rules and transition validations are satisfied. Human-only approval decisions and sensitive complaint closure must remain under Supervisor control. Record approved human decisions and failed/denied attempts. **Evidence:** approval workflow, transition, and audit tests.

#### Integration, Evaluation & Release

- [ ] **T036 — Integrate the single agent with the approved tools.** Verify complete authorized investigation paths, structured evidence packages, citations, recommendations, reviewer routing, and safe handoff. Keep unresolved tool gaps explicit. **Evidence:** end-to-end integration tests.
- [ ] **T037 — Test normal, boundary, denied, and failure cases.** Reuse supplied agent/evaluation datasets and failure scenarios: SQL unavailable, vector store unavailable, MCP timeout, model rate limit, invalid state transition, approval rejected, insufficient/conflicting evidence, and execution-limit reached. **Evidence:** test outputs and defect log.
- [ ] **T038 — Validate audit and acceptance-criteria traceability.** Link Sprint 1 acceptance criteria to tests and recorded evidence; ensure separation of customer assertions, verified facts, policy evidence, generated analysis, and human decisions. **Evidence:** acceptance matrix and trace samples.
- [ ] **T039 — Prepare documentation, review, and handover.** Update README, architecture, known limitations, dependencies, and PR links. Use the assigned branch; request coach review and do not claim an approved release until validated. **Evidence:** PR and handover notes.

**Dependencies / open decisions:** Week 4 release approval and retrieval contract; no approved `create_complaint` tool; classification/urgency execution boundary; transaction-level lookup; role and API differences; status/approval lifecycle. Do not silently implement missing tool capabilities.

## Sprint 4 – Analyst Portal

- [ ] T040 Create complaint dashboard : Display complaint details and workflow status.

- [ ] T041 Display structured evidence : Present verified customer and complaint information.

- [ ] T042 Display policy evidence and citations : Present approved guidance and source information.

- [ ] T043 Display recommendations.

- [ ] T044 Create human approval interface : Allow supervisors to approve, reject, or request changes.

## Sprint 5 - Quality, Security & Validation

- [ ] T045 Validate acceptance criteria

- [ ] T046 Execute positive scenarios : Test normal complaint workflows.

- [ ] T047 Execute negative scenarios : Test invalid submissions and error conditions.

- [ ] T048 Execute edge scenarios : Test ambiguous complaints, duplicate complaints, and conflicting evidence.

- [ ] T049 Validate security controls : Verify access restrictions and authorization controls.