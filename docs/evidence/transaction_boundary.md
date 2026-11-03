
# Transaction Boundary — Complaint Creation

## Objective

Ensure that complaint creation and initial status event creation
are performed atomically.

## Transaction Boundary

The transaction includes two database operations:

1. Insert a new complaint.
2. Insert the corresponding initial status history event.

Both operations must succeed before the transaction is committed.

## Success Scenario

- Create the complaint.
- Create the initial status event.
- Commit the transaction.
- Return the created complaint.

## Failure Scenario

If either database operation fails:

- Roll back the transaction.
- Do not persist the complaint.
- Do not persist the initial status event.
- Return an appropriate API error.

## Implementation Decision

SQLAlchemy ORM will manage both database writes using the same
database session.

The repository will handle database writes and transaction
commit/rollback, while the service layer will continue to
handle business validation.

## Expected Result

No partially created complaint should remain in the database
after a transaction failure.
