# Domain Model Design Notes

## 1. Overview

This document describes the design decisions for the Banking Complaint Resolution Assistant domain models, updated for Week 3, Exercise 3.1.1.

The current implementation defines four SQLAlchemy ORM models in `src/models/models.py`:

- **Customer:** Stores customer identity and contact information.
- **Account:** Represents a bank account belonging to a customer.
- **Complaint:** Represents a customer complaint, its classification, priority, status, and optional analyst assignment.
- **ComplaintStatusEvent:** Represents a complaint status change, including the previous and new statuses, timestamp, and optional change metadata.

The models inherit from a SQLAlchemy `DeclarativeBase` and map to the SQLite tables `customer`, `account`, `complaint`, and `complaint_status_history`. They are ORM classes, **not Python dataclasses**. SQL operations and session management are handled by repositories and the database connection layer rather than by domain methods.

## 2. Controlled Values and Validation

### 2.1 Enumerations

Three Python `Enum` types restrict complaint-related values:

- **ComplaintCategory:** Fee Dispute, Service Delay, Transaction Error, Online Banking, Card Issue, Customer Service, Fraud Claim.
- **ComplaintPriority:** Critical, High, Medium, Low.
- **ComplaintStatus:** `OPEN`, `IN_PROGRESS`, `UNDER_REVIEW`, `CLOSED`.

SQLAlchemy uses `SAEnum` with a `values_callable` to store the enum **values**. At the API boundary, Pydantic schemas reject unsupported enum values with HTTP `422` responses.

### 2.2 ORM Model Validation

The `Complaint` model uses SQLAlchemy's `@validates("category", "status", "priority")` decorator to check values assigned to its controlled attributes. Incorrect Python types or unsupported string values raise `ValueError`; `priority` may be `None`.

`ComplaintStatusEvent` uses `@validates("new_status", "old_status")` to validate the statuses assigned to an event. `old_status` is optional; `new_status` must be a valid `ComplaintStatus`.

Unlike the initial design, validation is **not** implemented using dataclass `__post_init__()` methods. SQLAlchemy attribute validators are used instead.

### 2.3 Status Transitions

Complaint status changes follow the currently implemented workflow:

`OPEN → IN_PROGRESS → UNDER_REVIEW → CLOSED`

Allowed transitions are defined in `VALID_STATUS_TRANSITIONS`. The `Complaint.change_status()` method verifies the requested target status and transition before updating the complaint. On success it returns a `ComplaintStatusEvent` containing the old status, new status, and optional change metadata. The calling service/repository is responsible for persisting that event; returning it does not itself insert a database row.

Invalid transitions raise `ValueError` and leave the complaint's status unchanged. No transition is allowed from `CLOSED`.

**Specification note:** These implemented transition rules should still be checked against the approved business specification before production use.

## 3. Technical Design Decisions

### 3.1 Data Types and Defaults

The ORM column types reflect the banking data:

- `String` for identifiers and descriptive fields.
- `Numeric(15, 2)` for account balances, with a `Decimal("0.00")` default to avoid floating-point precision issues in stored financial values.
- `Date` for account opening dates.
- `DateTime` for customer creation dates, complaint receipt timestamps, and status-event timestamps, using callable `datetime.now` defaults where defined.
- Nullable fields for optional contact information, complaint account reference, priority, analyst assignment, and event metadata, as permitted by each model.

SQLAlchemy defaults such as `default=datetime.now` run when a database insertion occurs, not automatically merely because a Python object was constructed.

### 3.2 Identifiers and Relationships

The `generate_id(session, model)` helper generates model-specific, sequentially formatted identifiers:

- Customer: `CUS001`, `CUS002`, ...
- Account: `ACC001`, `ACC002`, ...
- Complaint: `CMP001`, `CMP002`, ...

It selects existing IDs, finds the largest matching numeric suffix, and increments it. Repositories use the helper when inserting new records. The account and complaint models reference related records with SQLAlchemy foreign keys.

**Limitation:** Reading the maximum existing suffix is not concurrency-safe. Simultaneous requests could calculate the same next identifier. A database-managed mechanism would be preferable in production.

### 3.3 Layer Responsibilities

- **ORM models:** Define entity mappings, controlled values, and complaint transition behavior.
- **Pydantic schemas:** Validate incoming API payloads.
- **Repositories:** Query, insert, and retrieve records through SQLAlchemy sessions.
- **Services:** Coordinate application operations and business workflows.
- **FastAPI routers:** Expose endpoints under `/bank`.

The ORM models contain database column declarations and foreign-key mappings, but no hand-written SQL queries or session-management code. This is different from a fully persistence-independent domain model.

### 3.4 Status History

`ComplaintStatusEvent` maps to `complaint_status_history`. Its integer `history_id` is generated by SQLite on insertion. The `change_status()` method creates an event object; saving it remains a separate persistence operation, which enables explicit control of audit-history writes.

## 4. Testing Strategy and Evidence

Tests are implemented with Pytest in `tests/test_domain_models.py`. The updated suite contains **12 passing tests**, as verified during development.

The suite covers:

1. Creating a customer using `POST /bank/customers` and checking its generated `CUS` identifier.
2. Creating an account using `POST /bank/accounts` and checking its generated `ACC` identifier.
3. Creating a complaint using `POST /bank/complaints` and checking its generated `CMP` identifier.
4. A valid transition from `OPEN` to `IN_PROGRESS`, including the returned status-event object.
5. Rejection of a direct `OPEN` to `CLOSED` transition.
6. Rejection of transitions from `CLOSED`.
7. API rejection of an invalid complaint category (`422`).
8. API rejection of an invalid complaint status (`422`).
9. API rejection of an invalid complaint priority (`422`).
10. ORM rejection of an invalid complaint category.
11. ORM rejection of an invalid complaint priority.
12. ORM rejection of an invalid status-event `new_status`.

Run the suite from the repository root with:

```powershell
python -m pytest tests/test_domain_models.py -v
```

**Test-environment limitation:** The API creation tests currently write to the development SQLite database (`bank_complaint.db`) and use some fixed IDs/account numbers. They therefore depend on existing data and may not be repeatable without cleanup. A future improvement is to use test fixtures with an isolated SQLite database and dynamically created related records.

## 5. Future Improvements

- Confirm the workflow transitions and controlled values against the approved project specification.
- Add isolated, repeatable database fixtures for API integration tests.
- Validate additional required fields and optional-value edge cases.
- Add tests covering status-event persistence and retrieval through the API.
- Use a concurrency-safe strategy for generating customer, account, and complaint identifiers.
- Ensure complaint status updates and history-event persistence occur within a single transaction in the service layer.
- Extend service-layer behavior in Exercise 3.1.2 while retaining separation between routers, services, repositories, and models.
