# Assisted Journey

## Complaint handling with the proposed assistant and without escalation

```text
┌────────────────────┐
│      CUSTOMER      │
└─────────┬──────────┘
          │ Submit Complaint
          ▼
┌────────────────────┐
│       INTAKE       │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Human Activities
          │ - Review submitted complaint
          │ - Confirm complaint intake
          │
          │ SQL Facts
          │ - Customer information
          │ - Complaint intake data
          │
          │ Generated Assistance
          │ - Validate required fields
          │ - Identify missing information
          │ - Suggest complaint category
          │ - Calculate urgency using the
          │   approved rule table
          │
          │ Human Decisions
          │ - Accept or modify category
          │ - Accept or modify urgency
          │
          │ Systems
          │ - Complaint Management System
          │ - AI Assistant
          ▼
┌────────────────────┐
│   INVESTIGATION    │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Human Activities
          │ - Review complaint context
          │ - Investigate complaint
          │
          │ SQL Facts
          │ - Complaint records
          │ - Customer records
          │
          │ Generated Assistance
          │ - Complaint summary
          │ - Key fact extraction
          │ - Suggested evidence checklist
          │
          │ Human Decisions
          │ - Determine investigation path
          │
          │ Systems
          │ - Complaint Management System
          │ - AI Assistant
          ▼
┌────────────────────┐
│  EVIDENCE SEARCH   │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ SQL Facts
          │ - Transaction history
          │ - Complaint history
          │
          │ Document Retrieval
          │ - Complaint policies
          │ - Procedures
          │ - Reference documents
          │
          │ Generated Assistance
          │ - Evidence summary
          │ - Relevant document references
          │
          │ Human Decisions
          │ - Validate evidence relevance
          │ - Accept or reject retrieved evidence
          │
          │ Systems
          │ - SQL Data Sources
          │ - Document Repository
          │ - AI Assistant
          ▼
┌────────────────────┐
│   RECOMMENDATION   │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ SQL Facts
          │ - Investigation findings
          │
          │ Document Retrieval
          │ - Applicable complaint policies
          │
          │ Generated Assistance
          │ - Proposed resolution
          │ - Draft rationale
          │
          │ Human Decisions
          │ - Approve, modify or reject
          │   recommendation
          │
          │ Systems
          │ - Complaint Management System
          │ - AI Assistant
          ▼
┌────────────────────┐
│      RESPONSE      │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Generated Assistance
          │ - Draft customer response
          │ - Summarize rationale
          │
          │ Human Decisions
          │ - Edit response if required
          │ - Approve response
          │ - Send response to customer
          │
          │ Systems
          │ - Complaint Management System
          │ - Communication Channels
          │ - AI Assistant
          ▼
┌────────────────────┐
│      CLOSURE       │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ SQL Facts
          │ - Final complaint status
          │
          │ Generated Assistance
          │ - Case summary
          │ - Audit summary
          │
          │ Human Decisions
          │ - Confirm closure
          │
          │ Systems
          │ - Complaint Management System
          │ - AI Assistant
          ▼
┌────────────────────┐
│    CASE CLOSED     │
└────────────────────┘
```

## Complaint handling with the proposed assistant and with escalation

```text
┌────────────────────┐
│      CUSTOMER      │
└─────────┬──────────┘
          │ Submit Complaint
          ▼
┌────────────────────┐
│       INTAKE       │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Human Activities
          │ - Review submitted complaint
          │ - Confirm complaint intake
          │
          │ SQL Facts
          │ - Customer information
          │ - Complaint intake data
          │
          │ Generated Assistance
          │ - Validate required fields
          │ - Identify missing information
          │ - Suggest complaint category
          │ - Calculate urgency using the
          │   approved rule table
          │
          │ Human Decisions
          │ - Accept or modify category
          │ - Accept or modify urgency
          ▼
┌────────────────────┐
│   INVESTIGATION    │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ SQL Facts
          │ - Complaint records
          │ - Customer records
          │
          │ Generated Assistance
          │ - Complaint summary
          │ - Key fact extraction
          │ - Suggested investigation focus
          │
          │ Human Decisions
          │ - Determine investigation path
          ▼
┌────────────────────┐
│  EVIDENCE SEARCH   │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ SQL Facts
          │ - Transaction history
          │ - Complaint history
          │
          │ Document Retrieval
          │ - Complaint policies
          │ - Procedures
          │ - Reference documents
          │
          │ Generated Assistance
          │ - Evidence summary
          │ - Relevant document references
          │
          │ Human Decisions
          │ - Validate evidence relevance
          ▼
┌────────────────────┐
│   RECOMMENDATION   │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Generated Assistance
          │ - Proposed resolution
          │ - Draft rationale
          │
          │ Human Decisions
          │ - Review recommendation
          │ - Submit escalation
          ▼
┌────────────────────┐
│      APPROVAL      │
│ Supervisor/Reviewer│
└─────────┬──────────┘
          │
          │ Generated Assistance
          │ - Recommendation summary
          │ - Evidence summary
          │ - Policy references
          │
          │ Human Decisions
          │ - Approve recommendation
          │ - Reject recommendation
          │ - Request additional investigation
          │ - Make final decision
          │
          │ Human Control
          │ - Sensitive outcomes require
          │   supervisor approval before
          │   any action is taken
          ▼
┌────────────────────┐
│      RESPONSE      │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Human Activities
          │ - Review response draft
          │ - Verify accuracy
          │ - Send final response
          │
          │ Generated Assistance
          │ - Customer response draft
          │ - Resolution summary
          │
          │ Systems
          │ - Complaint Management System
          │ - Communication Channels
          │ - AI Assistant
          ▼
┌────────────────────┐
│      CLOSURE       │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Human Activities
          │ - Verify all actions completed
          │ - Confirm complaint resolution
          │ - Close case
          │
          │ SQL Facts
          │ - Final complaint status
          │ - Resolution data
          │
          │ Generated Assistance
          │ - Case summary
          │ - Audit summary
          │ - Closure documentation
          │
          │ Human Decisions
          │ - Confirm case closure
          │
          │ Systems
          │ - Complaint Management System
          │ - AI Assistant
          ▼
┌────────────────────┐
│    CASE CLOSED     │
└────────────────────┘
```