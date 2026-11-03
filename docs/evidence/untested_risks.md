## 1. Escalation Rules

**Risk:** Escalation criteria are documented in POL-002 (Complaint Escalation Matrix, version 1.4), but no corresponding implementation was identified in the current Python source code.

The coach confirmed that POL-002 defines the escalation criteria for this exercise.

**Business rules:**

- **Immediate escalation:** Suspected unauthorized transactions, threats of harm, legal notices, regulator correspondence, or confirmed data exposure.
- **Supervisor review:** High-priority complaints, repeated unresolved complaints, or proposed financial redress.
- **Standard handling:** Routine complaints without applicable escalation triggers.

**Testing gap:** Unit tests cannot currently verify these escalation decisions because no escalation evaluation function or service has been identified.

**Recommendation:** Add parameterized escalation tests once the decision logic is implemented. Ensure each escalation decision can be traced to the triggering complaint fact and the relevant POL-002 section.

**Status:** Pending implementation clarification. No escalation logic was added as part of this unit-testing exercise.

## 2. Database Constraints

**Risk:** Some required fields are enforced by SQLAlchemy database constraints rather than direct Python validation.

**Testing gap:** Unit tests verify Pydantic validation but do not test database constraints.

**Recommendation:** Verify database constraints through integration tests.

## 3. Fake Repositories

**Risk:** Fake repositories do not reproduce every behavior of the real database.

**Testing gap:** SQL transactions, rollbacks and database failures are not covered by the unit test suite.

**Recommendation:** Continue testing database-specific behavior through integration tests.