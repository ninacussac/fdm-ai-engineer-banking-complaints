# Week 3 — Completed Code Review Checklist

## Review scope

Review of the Week 3 FastAPI complaint API and integration tests.

References:
- `spec.md`
- `us_002.md`
- `code_review_checklist.md`
- `tests/integration/`
- `docs/evidence/integration_test_report.txt`

## Checklist

| Review criterion | Status | Findings |
|---|---|---|
| Spec alignment | Gap identified | US2-003 (`Needs Information`) is not implemented in the reviewed API. Missing fields currently produce HTTP 422. |
| Correctness | Passed with limitations | Complaint creation and status updates use transactions and rollback handling. |
| Layer boundaries | Passed | Business validation is handled by the service, database persistence by repositories, and HTTP responses by routers. |
| Parameterized SQL | Passed for reviewed code | SQLAlchemy ORM queries are used without visible string-concatenated SQL. |
| Secrets/data protection | Action required | `.env` is ignored by Git. Authentication and authorization controls were not found in the reviewed application code. |
| Tests | Passed | 10 integration tests passed repeatedly, including in reverse order. |
| Errors/logging | Improvement needed | Structured logging and correlation IDs are implemented. Some endpoints use inconsistent error handling. |
| Documentation | Passed with limitations | Specification, acceptance evidence, test report and setup documentation are referenced. |

## Review findings

### CR-001 — Authentication and authorization

**Severity:** Potential blocking

Complaint endpoints do not show authentication or authorization enforcement.

**Risk:** Unauthorized access to complaint data if the API is exposed.

**Action:** Confirm the intended scope and whether external access controls exist. Implement authorization before using real customer data.

**Status:** Open — Coach decision required.

### CR-002 — Inconsistent API error responses

**Severity:** Non-blocking

The complaint creation endpoint uses `HTTPException` while other endpoints use the standardized `AppError` format.

**Action:** Standardize error responses.

**Status:** Resolved.

**Resolution:** Replaced HTTPException with AppError in the complaint creation endpoint.

**Evidence:** Added test_create_complaint_with_unknown_customer to verify the HTTP 422 response, standardized error code, safe message and correlation ID.

**Test result:** 11 integration tests passed.

### CR-003 — Shared FastAPI testing state

**Severity:** Non-blocking

**Finding:** Integration tests use the shared
app.state.testing flag to disable normal database
initialization.

**Resolution:** Keep the current implementation for
sequential integration tests.

**Justification:** Each test uses a temporary SQLite
database, and the application state is reset in a
finally block.

**Future improvement:** Consider an application factory
to support independent application instances and
parallel testing.

**Status:** Deferred — Non-blocking.

### CR-004 — SQLAlchemy fixture cleanup

**Severity:** Non-blocking

The test database engine may not be disposed of if fixture setup fails before `yield`.

**Action:** Use `try/finally` to guarantee cleanup.

**Status:** Resolved.

**Resolution:** Added a try/finally block to the test_db fixture
to guarantee SQLAlchemy engine cleanup, even if fixture setup fails.

**Evidence:** Updated tests/integration/conftest.py.

**Test result:** 11 integration tests passed.

### CR-005 — Audit actor traceability

**Severity:** Non-blocking

**Finding:** The `changed_by` field is optional in the ComplaintStatusEvent model.

**Resolution:** Keep the field optional for automatic events. Require actor identification when implementing human approval and final-decision workflows.

**Status:** Deferred — Future audit workflow.

**Reason:** Final-decision functionality is outside thescope of the current integration-testing PR.

## Positive findings

- Atomic complaint creation and status-event persistence.
- Transaction rollback handling.
- Temporary SQLite database for integration tests.
- Structured application logs.
- Correlation IDs in standardized API errors.
- `.env` excluded from Git tracking.

## Review decision

**Pending.**

The review cannot be considered approved until the potentially blocking security finding has been resolved or explicitly assessed by the coach.

Non-blocking comments must also be corrected or justified before closing the review.

## Final Regression Testing

After implementing CR-002 and CR-004, the complete unit and integration
test suites were executed.

Command:
`python -m pytest tests/unit tests/integration -v`

Result: **42 tests passed**.

Both corrections are validated on the review branch.

The authentication and authorization finding (CR-001) remains open,
pending explicit review and a decision from the coach.