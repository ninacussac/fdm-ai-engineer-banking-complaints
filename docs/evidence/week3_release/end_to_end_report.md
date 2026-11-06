# Week 3 Release — End-to-End Test Report

## 1. Objective

Validate the complete complaint lifecycle through the FastAPI endpoints and verify that complaint status changes are correctly persisted in the SQLite database.

The tests use a temporary SQLite database to avoid modifying development data.

## 2. Successful Scenario

**Test:** `test_week3_release_end_to_end`

**Steps performed:**

1. Create a complaint using `POST /complaints`.
2. Retrieve the initial status history using `GET /events`.
3. Verify that the initial status is `OPEN`.
4. Update the complaint status to `IN_PROGRESS` using `PATCH /complaints/{complaint_id}/status`.
5. Retrieve the updated status history.
6. Verify that two status events exist.
7. Query the SQLite database to confirm the complaint status and history were persisted.

**Result: PASSED**

The complaint was successfully created and updated. Both status events were stored correctly.

## 3. Failure Scenario

**Test:** `test_week3_release_invalid_status_transition`

**Steps performed:**

1. Create a complaint with status `OPEN`.
2. Attempt an invalid transition directly to `CLOSED`.
3. Verify that the API returns HTTP 409.
4. Verify that the response contains `INVALID_STATUS_TRANSITION`.
5. Confirm that the complaint remains `OPEN`.
6. Confirm that no additional status-history event was created.

**Result: PASSED**

The invalid transition was rejected without modifying the complaint or creating an additional history event.

## 4. Test Environment

- Framework: FastAPI
- Database: SQLite
- Test framework: pytest
- HTTP client: FastAPI TestClient
- Database isolation: Temporary SQLite database using pytest fixtures

## 5. Test Execution

**Command:**

`python -m pytest tests/integration/test_week3_release_e2e.py -v`

**Result: 2 tests passed.**

## 6. Conclusion

Both end-to-end scenarios passed successfully.

The tests demonstrate that the complaint lifecycle works as expected for the tested operations, status-history changes are persisted correctly, and an invalid status transition does not modify existing data.

Additional transaction rollback evidence is verified separately in the integration test suite.