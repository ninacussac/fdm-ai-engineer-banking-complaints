# Controlled Investigation Agent

## 1. Agent Purpose

The Controlled Investigation Agent supports banking complaint management by coordinating complaint creation, information retrieval, classification, urgency assessment, policy retrieval, and evidence-based recommendations.

The agent allows authorized users to create new complaints, access existing complaint and customer information, and review complaint statuses.

It assists investigations by identifying one or more relevant complaint categories, assessing urgency based on available case information, retrieving applicable banking policies through the existing RAG service, and recommending appropriate next steps.

The agent reuses existing database, domain, and RAG services rather than duplicating their functionality.

All operations must respect access controls, data validation rules, evidence traceability, and human oversight.

Complaint creation remains a business capability of the overall system but is not available to the initial Controlled Investigation Agent without an approved tool interface. The agent must not autonomously approve compensation, resolve complaints, execute financial transactions, or bypass mandatory human approvals.

## 2. Agent Scope

### 2.1 In Scope

The Controlled Investigation Agent shall support the following operations:

**FR-01 — Complaint Creation**

The agent shall assist authorized users in creating new banking complaints.

It shall collect the required information, validate the proposed complaint data, and present a summary for human review.

A complaint shall only be persisted after explicit confirmation from an authorized user.

The creation operation shall use existing complaint management services. Authorization, input validation, and duplicate-submission protection shall be enforced by the application, independently of any LLM decision.

Confirmation shall apply to the exact complaint data presented to the complaint analyst; changed data shall require renewed confirmation.

*Implementation Dependency*

Complaint creation remains part of the original business requirements. However, the approved MCP tool catalogue does not currently include a `create_complaint` tool.

Therefore, the initial Controlled Investigation Agent shall not execute complaint creation through an unapproved tool. This capability remains pending an approved interface and the required human confirmation controls.

**FR-02 — Complaint Status Retrieval**

The agent shall retrieve and display the current status of an existing complaint using its unique complaint identifier.

The operation shall be read-only and shall not trigger any status transition.

**FR-03 — Complaint Details Retrieval**

The agent shall retrieve available complaint details, including relevant case information and complaint history, through existing authorized database services.

The agent shall not modify retrieved complaint records.

**FR-04 — Customer Information Retrieval**

The agent shall retrieve customer information relevant to an authorized complaint investigation.

Access shall be restricted according to the requesting user's permissions and the minimum information required for the task.

The agent shall not expose customer information to unauthorized users.

**FR-05 — Complaint Classification**

The agent shall analyze complaint information and propose one or more relevant categories using the existing approved category taxonomy.

*Initial Classification*

Before complaint creation, the agent shall propose an initial classification based on the information provided by the customer.

The proposed classification shall include a justification and shall be presented for human review before complaint creation is confirmed.

*Reclassification During Investigation*

The agent may reassess complaint classification when new relevant information becomes available during an investigation.

Any proposed change shall include the reason for reclassification and the evidence supporting it.

The agent shall not modify an existing complaint's stored classification without explicit authorization and confirmation.

If the available information is insufficient, the agent shall report the uncertainty and request human review.

**FR-06 — Urgency Assessment**

The agent shall evaluate complaint urgency based on available complaint information and approved business rules.

*Initial Urgency Assessment*

Before complaint creation, the agent shall propose an initial priority level using the existing priority taxonomy.

The proposal shall include a justification and shall be presented to the complaint analyst for review.

*Urgency Reassessment During Investigation*

The agent may reassess urgency when new relevant information becomes available.

The agent shall identify any proposed change in priority and explain the supporting evidence.

Any modification to the stored priority shall require authorization and explicit human confirmation.

The agent shall not invent priority criteria, override existing business rules, or treat its proposed priority as an approved operational decision.

**FR-05/FR-06 — Traceability Requirements**

The agent shall distinguish between proposed and persisted classifications and priority levels.

For each assessment or reassessment, the agent shall record, within the authorized investigation trace:

- The assessment type (initial or reassessment).
- The proposed categories and priority.
- The supporting evidence and justification.
- Any difference from the currently stored values.
- The human review outcome, where applicable.

A rejected proposal shall not alter persisted complaint information.

**FR-07 — Policy Information Retrieval**

The agent shall use the existing RAG service to retrieve applicable banking policies, procedures, and approval requirements.

Retrieved evidence shall respect document access restrictions, version requirements, and citation validation rules.

If the available policy evidence is insufficient or conflicting, the agent shall report the limitation rather than produce an unsupported conclusion.

**FR-08 — Evidence-Based Recommendations**

The agent shall generate recommendations for the next appropriate investigation steps based on complaint information, classification, urgency assessment, and retrieved policy evidence.

Recommendations shall distinguish verified facts, applicable policies, assumptions, and missing information.

The agent may recommend escalation or human approval but shall not execute these decisions autonomously.

### 2.2 Out of Scope

The Controlled Investigation Agent shall not:

1. Create complaints without explicit confirmation from an authorized user.
2. Autonomously approve or reject complaints, compensation requests, refunds, or financial adjustments.
3. Modify complaint statuses or existing complaint records without a separately authorized workflow.
4. Execute financial transactions or customer account modifications.
5. Communicate binding complaint-resolution decisions to customers.
6. Bypass access controls, document restrictions, or mandatory human approvals.
7. Invent customer information, complaint facts, policy rules, or supporting citations.
8. Treat its own classification, urgency assessment, or recommendations as formally approved operational decisions.

### 2.3 Human Oversight

The agent shall operate as a controlled decision-support system.

Human confirmation is mandatory before complaint creation.

Complaint classifications, urgency assessments, and recommendations shall remain reviewable and correctable by authorized users.

Actions requiring formal banking approval shall remain outside the agent's autonomous authority.

### 2.4 Reuse of Existing Components

The agent shall reuse existing complaint domain models, database access services, and RAG retrieval and answer-generation services.

The agent shall not introduce duplicate implementations of capabilities already provided by the banking complaint application.

The agent may propose tool calls dynamically, but an application-controlled layer shall validate tool allowlisting, user authorization, inputs, and mandatory confirmations before execution.

Any necessary extension to an existing interface or data model shall be documented and reviewed before implementation.

### 2.5 Tool Integration Requirement

The Controlled Investigation Agent shall perform authorized banking complaint operations through well-defined tool interfaces that reuse existing application services.

Tool capabilities shall be identified and documented in the tool catalogue. Their MCP contracts and server implementation shall be defined in subsequent exercises.

The agent shall not bypass existing business rules, access controls, or human approval requirements when invoking tools.

## 3. RAG Integration Strategy

### 3.1 Hybrid Retrieval Approach

The Controlled Investigation Agent shall follow a hybrid retrieval approach, invoking the existing RAG service only when policy knowledge is required.

Simple data retrieval operations, such as viewing complaint details, complaint status, or authorized customer information, shall use existing database services without unnecessary RAG calls.

The agent shall invoke the RAG service when answering policy-related questions or generating recommendations that depend on banking policies, procedures, escalation requirements, or approval rules.

### 3.2 RAG Invocation Rules

The agent shall:

1. Identify whether the user request requires complaint data, policy evidence, or both.
2. Use authorized database services for factual complaint and customer information.
3. Invoke the existing RAG service when policy interpretation or policy-grounded recommendations are required.
4. Preserve the citations, evidence limitations, and support status returned by the RAG service.
5. Avoid presenting unsupported policy claims as verified recommendations.
6. Request additional information or human review when policy evidence is insufficient, ambiguous, or conflicting.

### 3.3 Reuse of Existing Services

The agent shall reuse the existing RAG retrieval, embedding, vector storage, generation, and citation validation components.

The agent shall not implement a separate policy retrieval pipeline.

The choice between Gemini and Ollama shall remain configurable through the existing provider configuration.

### 3.4 RAG Failure Handling

If the RAG service is unavailable, returns insufficient evidence, or reports conflicting policy information, the agent shall not invent a policy-based recommendation.

The agent may continue independent authorized operations that do not require policy evidence.

Any unresolved policy-dependent action shall be deferred for additional evidence or human review.

## 4. Cross-Cutting Requirements

**NFR-01 — Data Minimization**

The agent shall process only information needed for the authorized task.

**NFR-02 — Evidence Traceability**

The agent shall distinguish retrieved facts, policy evidence, generated assessments, and approved actions. Citations and RAG limitations shall remain visible in any policy-dependent recommendation.

**NFR-03 — Controlled Tool Execution**

An application-controlled executor shall validate tool selection and parameters independently of the LLM. Only explicitly registered tools may be invoked. Creation and authorized updates shall require human confirmation.

**NFR-04 — Safe Failure**

Authorization denial, unavailable services, missing or contradictory evidence, invalid tool requests, and execution-limit breaches shall lead to controlled failure or human review. The agent shall not bypass controls to complete a task.

**NFR-05 — Investigation Trace and Sensitive Data**

Relevant tool calls, outcomes, human decisions, and errors shall be traceable subject to applicable access and retention rules. Secrets and real customer data shall not be committed to the repository.
