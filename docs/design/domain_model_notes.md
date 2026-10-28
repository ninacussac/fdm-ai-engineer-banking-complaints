# Domain Model Design Notes

## 1. Overview

This document describes the design decisions made for the Python domain models of the Banking Complaint Resolution Assistant, as part of Week 3, Exercise 3.1.1.

The implementation introduces four domain models:

- **Customer:** Represents a bank customer and their personal information.
- **Account:** Represents a bank account associated with a customer.
- **Complaint:** Represents a customer complaint, including its category, priority, current status, and assigned analyst.
- **ComplaintStatusEvent:** Represents a complaint status change and stores information about the previous status, new status, timestamp, and responsible employee.

The models are implemented using Python dataclasses with type annotations.

Their attributes are aligned with the existing database schema developed during Week 2.

The domain layer remains independent of SQL queries, database repositories, and web frameworks.

## 2. Controlled Values and Validation

### 2.1 Enumerations

Three Python enumerations (`Enum`) have been implemented to control complaint-related values:

- **ComplaintCategory:** Defines the seven complaint categories identified in the Week 2 database, including Fee Dispute, Transaction Error, Fraud Claim, and Customer Service.
- **ComplaintPriority:** Defines four priority levels: Low, Medium, High, and Critical.
- **ComplaintStatus:** Defines four complaint statuses: OPEN, IN_PROGRESS, UNDER_REVIEW, and CLOSED.

These enumerations ensure consistency with the existing database values and prevent the use of arbitrary strings in the domain models.

### 2.2 Domain Validation

The `Complaint` and `ComplaintStatusEvent` models use the `__post_init__()` method to validate controlled values during object initialization.

Invalid categories, priorities, or statuses raise a `ValueError`.

Optional fields, such as `Complaint.priority` and `ComplaintStatusEvent.old_status`, can be set to `None` when no value is available.

### 2.3 Status Transitions

Complaint status changes are managed through the `change_status()` method.

The proposed workflow is:

`OPEN → IN_PROGRESS → UNDER_REVIEW → CLOSED`

Allowed transitions are explicitly defined in the `VALID_STATUS_TRANSITIONS` dictionary.

The method checks whether a requested transition is permitted before modifying the complaint status.

When a transition is valid, a `ComplaintStatusEvent` object is created to represent the change.

Invalid transitions raise a `ValueError`, leaving the complaint status unchanged.

**Note:** The transition rules are currently proposed business rules and must be confirmed against the approved project specification.

## 3. Technical Design Decisions

### 3.1 Python Data Types

Python type annotations were selected to match the existing Week 2 database schema:

- `str` for identifiers, names, and text fields.
- `Decimal` for account balances to avoid floating-point precision issues in financial calculations.
- `date` for account opening dates.
- `datetime` for customer creation dates, complaint reception timestamps, and status change timestamps.
- `None` for optional fields, such as complaint account references, priorities, and assigned analysts.

The `field(default_factory=...)` mechanism is used to generate default values for timestamps and account balances.

### 3.2 Database Independence

The domain models do not contain SQL queries or database connection logic.

Relationships between entities are represented using identifiers, such as `customer_id`, `account_id`, and `complaint_id`.

### 3.3 Status History

The `ComplaintStatusEvent` model represents changes in complaint status.

The `history_id` field is optional because the database automatically generates this identifier when the event is inserted.

The `change_status()` method returns a status event after a valid transition, allowing the persistence layer to save the event separately.

## 4. Testing Strategy

Unit tests were implemented using Pytest in `tests/test_domain_models.py`.

The initial test suite contains eight tests covering:

- Successful complaint creation.
- Rejection of invalid complaint categories.
- Rejection of invalid complaint statuses.
- Rejection of invalid complaint priorities.
- Successful status transitions and event creation.
- Rejection of invalid status transitions without modifying the complaint.
- Successful creation of complaint status events.
- Rejection of complaint status events with invalid new statuses.

All eight initial tests passed.

These tests verify the domain logic independently of the database and web framework.

## 5. Future Improvements

Potential improvements include:

- Confirming the allowed status transitions against the approved business specification.
- Adding validation for mandatory identifiers and text fields.
- Adding tests for optional values and invalid previous event statuses.
- Integrating the domain models into the service layer during Exercise 3.1.2.
- Connecting the service layer to the existing database repositories while keeping SQL outside the domain models.