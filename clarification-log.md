# Clarification Log

Project: Banking Complaint Resolution Assistant
Feature: Complaint Intake, Classification, Evidence Retrieval, Recommendation and Human Review
Log owner: Business Analyst
Status values: Open, Answered, Deferred, Rejected, Superseded


List : 


- rule table
- How does it knoes if it should be escalated ?
- How to differenciate when we need defined records from generated reasoning ?
- How does the RAG find the relevant passages and returns them with source information ?
- How do we define for each tool a defined input schema, output schema, validation rules, permissions, error behaviour and audit requirements. 
- How does the assistant know which tool to use ? Like "used the approved SQL" 
- Where are the data of the client records etc ?
- How do we create the relational data model ?
- What is present in the portal used by the analyst ?
- How do we know that a case is sensitive ?
- 


## CL-001: Urgency Rule Selection

- Category: Business Rules
- Question: The Domain Guide provides urgency rules for the transaction dispute scenario. Are equivalent urgency rules available for Fees, Digital Banking, Service Quality, Mortgage Servicing and Account Access complaints?
- Why it matters: Consistent complaint prioritization requires defined urgency rules for all supported complaint categories.
- Source/Owner: Coach / Product Owner
- Decision: Not specified in the supplied materials.
- Status: Open
- Decision Date: TBD

## CL-002: Escalation Criteria

- Category: Workflow
- Question: How does the system determine whether a complaint should be escalated?
- Why it matters: Escalation directly affects routing, approval workflows, and human-review requirements.
- Source/Owner: Domain Guide / Product Owner
- Decision: High-priority and sensitive scenarios are routed for human review. However, complete escalation criteria for all complaint categories are not fully defined in the supplied materials.
- Reference: Banking_Complaint_Resolution_Domain_Guide Sections 8 and 11.3.
- Status: Partially Answered
- Decision Date: 2026-10-15

## CL-003: Structured Facts vs Generated Reasoning

- Category: Evidence Management
- Question: How does the solution distinguish between structured records and generated reasoning?
- Why it matters: Incorrectly mixing facts and generated analysis may reduce traceability and trust.
- Source/Owner: Domain Guide
- Decision: Structured operational facts, retrieved policy evidence, and generated analysis must remain separate throughout the workflow.
- Reference: Banking_Complaint_Resolution_Domain_Guide Sections 7 and 11.3.
- Status: Answered
- Decision Date: 2026-10-15

## CL-004: RAG Retrieval Logic

- Category: Knowledge Retrieval
- Question: How does the RAG service determine which policy passages are relevant?
- Why it matters: Policy retrieval affects recommendation quality and traceability.
- Source/Owner: Product Owner / Coach
- Decision: The materials state that RAG retrieves approved guidance and returns citations including source document, section, version, and effective date. The retrieval and ranking methodology is not specified.
- Reference: Banking_Complaint_Resolution_Assistant_Project_Brief and Banking_Complaint_Resolution_Domain_Guide.
- Status: Open
- Decision Date: TBD

## CL-005: Tool Interface Requirements

- Category: Tools
- Question: How should input schemas, output schemas, permissions, validation rules, error handling, and audit requirements be defined for each tool?
- Why it matters: Consistent tool behavior is required for testing and integration.
- Source/Owner: Coach / Technical Lead
- Decision: The project brief requires every tool to have defined inputs, outputs, validation rules, permissions, error behavior, and audit requirements, but no standards or templates are provided.
- Reference: Banking_Complaint_Resolution_Assistant_Project_Brief.
- Status: Open
- Decision Date: TBD

## CL-006: Tool Selection Logic

- Category: Agent Workflow
- Question: How does the assistant determine which approved tool should be used for a given task?
- Why it matters: Tool-selection behavior affects workflow consistency and reproducibility.
- Source/Owner: Coach / Product Owner
- Decision: The supplied materials state that an agent may select among approved tools and coordinate workflow steps, but the selection criteria are not defined.
- Reference: Banking_Complaint_Resolution_Domain_Guide Section 9 and Banking_Complaint_Resolution_Assistant_Project_Brief.
- Status: Open
- Decision Date: TBD

## CL-007: Source of Customer Records

- Category: Data
- Question: Where are customer, account, complaint, transaction, fee, and service-request records stored?
- Why it matters: Data access is required before APIs, SQL queries, and workflows can be implemented.
- Source/Owner: Project Brief
- Decision: The project uses synthetic training data and expects a relational data model containing customers, accounts, complaints, transactions, fees, service requests, and status history. The actual storage implementation is not defined.
- Reference: Banking_Complaint_Resolution_Assistant_Project_Brief.
- Status: Partially Answered
- Decision Date: 2026-10-15

## CL-008: Relational Data Model Design

- Category: Data Model
- Question: How should the relational data model be designed?
- Why it matters: Data structure impacts APIs, workflows, testing, and traceability.
- Source/Owner: Coach / Technical Lead
- Decision: The project requires a relational model containing customers, accounts, complaints, transactions, fees, service requests, and status history, but detailed relationships and schema definitions are not provided.
- Reference: Banking_Complaint_Resolution_Assistant_Project_Brief.
- Status: Open
- Decision Date: TBD

## CL-009: Analyst Portal Contents

- Category: User Interface
- Question: What information must be displayed in the analyst portal?
- Why it matters: User-interface requirements affect workflow design and testing.
- Source/Owner: Project Brief
- Decision: The portal must clearly separate verified facts, policy evidence, generated analysis, and human decisions. Additional screen-level requirements are not specified.
- Reference: Banking_Complaint_Resolution_Assistant_Project_Brief.
- Status: Partially Answered
- Decision Date: 2026-10-15

## CL-010: Sensitive Case Definition

- Category: Governance
- Question: How do we determine whether a case is considered sensitive?
- Why it matters: Sensitive cases require routing, approval, and audit controls.
- Source/Owner: Product Owner
- Decision: The supplied material identifies final approvals, compensation decisions, reimbursement decisions, and legal or regulatory judgments as sensitive decisions requiring human involvement. A complete sensitive-case classification framework is not provided.
- Reference: Banking_Complaint_Resolution_Domain_Guide Section 5 and Banking_Complaint_Resolution_Assistant_Project_Brief.
- Status: Partially Answered
- Decision Date: 2026-10-15

## CL-011: Required Programming Languages and Frameworks

- Category: Technical Architecture
- Question: Are specific programming languages, frameworks, or technology stacks required for the implementation of the Banking Complaint Resolution Assistant?
- Why it matters: Technology choices affect architecture decisions, project planning, task breakdown, testing strategy, deployment approach, and team collaboration.
- Source/Owner: Coach / Technical Lead
- Decision: The project roadmap references technologies and components such as complaint APIs, RAG services, MCP tools, LangGraph workflows, and a React analyst portal. However, the supplied materials do not explicitly mandate a specific backend language, framework, database technology, or implementation stack.
- Reference: Banking_Complaint_Resolution_Assistant_Project_Brief.docx
- Impact: Technology selection remains a project decision and may require confirmation from the coach before implementation begins.
- Status: Open
- Decision Date: TBD