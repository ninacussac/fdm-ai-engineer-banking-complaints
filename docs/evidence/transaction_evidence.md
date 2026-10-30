# Transaction Evidence — Atomic Complaint Creation

## Objective

Ensure that complaint creation and initial status event creation are atomic.

## Transaction Implementation

Both database inserts are executed in the same SQLAlchemy session.

- `db.flush()` inserts the complaint without committing.
- The initial status event is inserted.
- `db.commit()` confirms both operations.
- `db.rollback()` cancels the transaction if an error occurs.

## Test Results

**Success scenario**

Test: `test_create_complaint_with_initial_event`

Result: PASSED

The complaint and its initial status event were successfully saved.

**Failure scenario**

Test: `test_rollback_when_event_fails`

Result: PASSED

A simulated exception during initial status event insertion triggered a rollback. The number of complaints remained unchanged.

- The API returns HTTP 500 with a generic error message.
- Internal database errors are not exposed to the client.
- No partial complaint remains after rollback.

## Idempotency Consideration

Currently, repeated POST requests can create separate complaints.

A possible improvement would be to introduce an idempotency key provided by the client. Repeated requests using the same key would return the original creation result rather than creating duplicate complaints.

This improvement is documented but not implemented in the current exercise.

## Conclusion

The transaction tests confirm that complaint creation and initial status event creation succeed together, and that a failure during the second operation does not leave an additional complaint in the database.

## Final Test Results

Command: `python -m pytest -v`

Result: 33 passed.