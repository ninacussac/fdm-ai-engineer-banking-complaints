# Alignment Notes

## Purpose

Review the assisted journeys against the specification to confirm that no new behavior was introduced and that all proposed capabilities can be traced to documented requirements.

# Journey Capability Traceability

## Intake Validation

### Journey Capability
- Validate required fields.
- Identify missing information.

### Specification Reference
- Scope: "Validate intake"
- Error Condition: "If a required field is absent, set the state to Needs Information."
- Acceptance Criteria: "Given a complaint with missing required information, the complaint status shall be set to Needs Information.

## Complaint Classification

### Journey Capability
- Suggest complaint category.
- Analyst reviews category assignment.

### Specification Reference
- Scope: "Classify the complaint."
- Core Flows: "The AI system classifies the complaint into one or more categories."
- Business Rules: "A complaint may belong to multiple categories."

## Urgency Calculation

### Journey Capability
- Calculate urgency using the approved rule table.
- Analyst validates the result.

### Specification Reference
- Scope: "Calculate the urgency of the complaint."
- Business Rules: "The system shall assign exactly one urgency level."
- High-Level Outputs:
  - Urgency score/type
  - Triggered rule

## Evidence Retrieval

### Journey Capability
- Retrieve structured evidence.
- Retrieve approved guidance.
- Provide document references.

### Specification Reference
- Scope:
  - "Retrieve structured evidence"
  - "Retrieve approved guidance"
- Non-Functional Requirements:
  - "Recommendations shall include supporting evidence and citations."
- Reliability Constraints:
  - "The system shall clearly separate verified facts, policy evidence, generated analysis, and human decisions."

## Escalation and Supervisor Review

### Journey Capability
- Escalated complaints are reviewed by a Supervisor.
- Supervisor may approve, reject, or request changes.

### Specification Reference
- Actors:
  - "Supervisor reviews escalated or sensitive cases and may approve, reject, escalate further, or request changes to a proposed action."
- Core Flows:
  - "If the review is escalated then it is routed to the Supervisor."

## Sensitive Outcome Approval

### Journey Capability
- Sensitive outcomes require Supervisor approval before action.

### Specification Reference
- Overview:
  - "Sensitive outcomes require human approval."
- Domain Rules:
  - "Sensitive outcomes require human approval."
- Success Criteria:
  - "100% of sensitive outcomes shall require human approval before action is taken."

## Customer Response Drafting

### Journey Capability
- Generate customer response draft.
- Human reviews and sends response.

### Specification Reference
- Scope:
  - "Communicate and monitor."
- Non-Goals:
  - "The assistant will not contact customers directly."

### Notes
The journey correctly keeps communication under human control.

