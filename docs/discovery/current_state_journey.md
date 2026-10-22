# Current State Journey

## Complaint handling without the proposed assistant and without escalation

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
          │ Activities
          │ - Receive complaint
          │ - Verify required information
          │ - Create complaint record
          │
          │ Systems
          │ - Complaint Management System
          │ - Intake Channel (email/web/phone)
          │
          │ Pain Points
          │ - Manual validation
          │ - Incomplete submissions
          │
          │ Delays
          │ - Waiting for assignment
          │ - Waiting for customer information
          │
          │ Rework
          │ - Contact customer for missing data
          ▼
┌────────────────────┐
│   INVESTIGATION    │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Activities
          │ - Review complaint
          │ - Understand issue
          │ - Identify impacted products,
          │   services or transactions
          │
          │ Systems
          │ - Complaint Management System
          │ - Banking Systems
          │
          │ Pain Points
          │ - Information scattered
          │ - Manual review effort
          │
          │ Rework
          │ - Re-open investigation if
          │   new information appears
          ▼
┌────────────────────┐
│  EVIDENCE SEARCH   │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Activities
          │ - Search supporting evidence
          │ - Retrieve transaction history
          │ - Retrieve customer interactions
          │ - Collect documentation
          │
          │ Systems
          │ - Document Repository
          │ - Transaction Systems
          │ - Customer Records
          │
          │ Pain Points
          │ - Multiple systems
          │ - Manual searches
          │
          │ Delays
          │ - Waiting for records
          │
          │ Rework
          │ - Repeat searches when
          │   evidence is incomplete
          ▼
┌────────────────────┐
│   RECOMMENDATION   │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Activities
          │ - Analyze evidence
          │ - Determine proposed resolution
          │ - Document rationale
          │
          │ Systems
          │ - Complaint Management System
          │
          │ Pain Points
          │ - Manual analysis
          │ - Inconsistent documentation
          │
          │ Delays
          │ - Time spent reviewing evidence
          │
          │ Rework
          │ - Recommendation updated after
          │   additional findings
          ▼
┌────────────────────┐
│      RESPONSE      │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Activities
          │ - Draft customer response
          │ - Communicate decision
          │
          │ Systems
          │ - Complaint Management System
          │ - Communication Channels
          │
          │ Handoffs
          │ - Analyst → Customer
          │
          │ Pain Points
          │ - Manual response drafting
          │
          │ Rework
          │ - Response revised after
          │   approval feedback
          ▼
┌────────────────────┐
│      CLOSURE       │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Activities
          │ - Update case status
          │ - Record outcome
          │ - Retain records
          │
          │ Systems
          │ - Complaint Management System
          │
          │ Pain Points
          │ - Administrative work
          │
          │ Delays
          │ - Processing backlog
          │
          │ Rework
          │ - Case may be reopened if
          │   new evidence appears
          ▼
┌────────────────────┐
│    CASE CLOSED     │
└────────────────────┘
```

## Complaint handling without the proposed assistant and with escalation


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
          │ Activities
          │ - Receive complaint
          │ - Verify required information
          │ - Create complaint record
          │
          │ Systems
          │ - Complaint Management System
          │ - Intake Channel (email/web/phone)
          │
          │ Pain Points
          │ - Manual validation
          │ - Incomplete submissions
          │
          │ Delays
          │ - Waiting for assignment
          │ - Waiting for customer information
          │
          │ Rework
          │ - Contact customer for missing data
          ▼
┌────────────────────┐
│   INVESTIGATION    │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Activities
          │ - Review complaint
          │ - Understand issue
          │ - Identify impacted products,
          │   services or transactions
          │
          │ Systems
          │ - Complaint Management System
          │ - Banking Systems
          │
          │ Pain Points
          │ - Information scattered
          │ - Manual review effort
          │
          │ Delays
          │ - Manual task by task research
          │
          │ Rework
          │ - Re-open investigation if
          │   new information appears
          ▼
┌────────────────────┐
│  EVIDENCE SEARCH   │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Activities
          │ - Search supporting evidence
          │ - Retrieve transaction history
          │ - Retrieve customer interactions
          │ - Collect documentation
          │
          │ Systems
          │ - Document Repository
          │ - Transaction Systems
          │ - Customer Records
          │
          │ Pain Points
          │ - Multiple systems
          │ - Manual searches
          │
          │ Delays
          │ - Waiting for records
          │
          │ Rework
          │ - Repeat searches when
          │   evidence is incomplete
          ▼
┌────────────────────┐
│   RECOMMENDATION   │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Activities
          │ - Analyze evidence
          │ - Determine proposed resolution
          │ - Document rationale
          │
          │ Systems
          │ - Complaint Management System
          │
          │ Pain Points
          │ - Manual analysis
          │ - Inconsistent documentation
          │
          │ Delays
          │ - Time spent reviewing evidence
          ▼
┌────────────────────┐
│     ESCALATION     │
│ Supervisor/Reviewer│
└─────────┬──────────┘
          │
          │ Activities
          │ - Review recommendation
          │ - Review supporting evidence
          │ - Assess risk and impact
          │ - Request clarification or changes
          │
          │ Systems
          │ - Complaint Management System
          │
          │ Handoffs
          │ - Analyst → Supervisor
          │ - Supervisor → Analyst
          │
          │ Pain Points
          │ - Manual review process
          │ - Review backlog
          │
          │ Delays
          │ - Waiting for supervisor availability
          │ - Waiting for analyst updates
          │
          │ Rework
          │ - Recommendation returned to analyst
          │   for clarification or revision
          ▼
┌────────────────────┐
│      APPROVAL      │
│ Supervisor/Reviewer│
└─────────┬──────────┘
          │
          │ Activities
          │ - Approve or reject recommendation
          │ - Confirm final resolution
          │
          │ Systems
          │ - Complaint Management System
          │
          │ Pain Points
          │ - Approval queue
          │
          │ Delays
          │ - Waiting for final decision
          ▼
┌────────────────────┐
│      RESPONSE      │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Activities
          │ - Draft customer response
          │ - Communicate decision
          │
          │ Systems
          │ - Complaint Management System
          │ - Communication Channels
          │
          │ Handoffs
          │ - Analyst → Customer
          │
          │ Pain Points
          │ - Manual response drafting
          │
          │ Delays
          │ - Approval-dependent response
          │
          │ Rework
          │ - Response revised after
          │   supervisor feedback
          ▼
┌────────────────────┐
│      CLOSURE       │
│ Complaint Analyst  │
└─────────┬──────────┘
          │
          │ Activities
          │ - Update case status
          │ - Record outcome
          │ - Retain records
          │
          │ Systems
          │ - Complaint Management System
          │
          │ Pain Points
          │ - Administrative work
          │
          │ Delays
          │ - Processing backlog
          │
          │ Rework
          │ - Case may be reopened if
          │   new evidence appears
          ▼
┌────────────────────┐
│    CASE CLOSED     │
└────────────────────┘
```