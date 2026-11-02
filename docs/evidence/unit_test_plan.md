# Unit Test Plan — Exercise 3.3.3

## Objective

Test the main business rules of the Complaint domain and ComplaintService using pytest.

Tests should be deterministic, behavior-focused and independent from the real database.

## 1. Happy Cases

| Test scenario | Expected behavior |
|---|---|
| Valid status transitions | Complaint status changes successfully |
| Valid complaint creation | Complaint is saved through the repository |
| Complaint creation without account | Complaint is accepted if the customer exists |
| Get existing complaint | Returns the requested complaint |
| Get all complaints | Returns the repository results |
| Get customer complaints | Returns complaints for an existing customer |

## 2. Boundary Cases

| Test scenario | Expected behavior |
|---|---|
| Priority is None | Accepted because priority is optional |
| Valid transition to CLOSED | Accepted from UNDER_REVIEW |
| Attempt to change a CLOSED complaint | Rejected |
| Escalation thresholds | Not implemented in the reviewed code; requires clarification |

## 3. Failure Cases

| Test scenario | Expected behavior |
|---|---|
| Invalid status transition | Raises ValueError |
| Invalid status value | Raises ValueError |
| Invalid category or priority | Raises ValueError |
| Missing required fields | Validation or persistence behavior must be checked separately |
| Customer does not exist | Raises ValueError |
| Account does not exist | Raises ValueError |
| Account belongs to another customer | Raises ValueError |
| Complaint does not exist | Raises ValueError |

## 4. Testing Approach

- Use pytest for unit tests.
- Use `pytest.mark.parametrize` for valid and invalid transitions.
- Create reusable fixtures in `tests/unit/conftest.py`.
- Use fake repositories instead of a real database.
- Verify returned values, status changes and expected exceptions.
- Avoid tests that depend on implementation details.
- Do not access the real SQLite database during unit tests.

## 5. Known Gaps

- Escalation indicators and thresholds were not found in the reviewed domain and service code.
- Required database fields are defined using SQLAlchemy `nullable=False`, which does not automatically validate all fields when a Python object is created.
- Additional validation rules may exist in the API schemas and are not covered by this initial domain/service test plan.