# Week 3 Release — Error Handling and Logging Evidence

## 1. Objective

Verify that the Banking Complaint Resolution Assistant API handles failure scenarios safely and produces structured logs for request traceability.

## 2. Test Execution

**Command:**

`python -m pytest tests/integration/test_complaint_api.py -v --log-cli-level=INFO`

**Result: 8 tests passed.**

Detailed evidence is available in `error_logging_test_output.txt`.

## 3. Error Handling Evidence

| Scenario | HTTP Status | Expected API Error | Result |
|---|---|---|---|
| Complaint not found | 404 | `COMPLAINT_NOT_FOUND` | PASSED |
| Invalid status transition | 409 | `INVALID_STATUS_TRANSITION` | PASSED |
| Invalid complaint data | 422 | `INVALID_COMPLAINT_DATA` | PASSED |
| Missing required field | 422 | `VALIDATION_ERROR` | PASSED |
| Database unavailable | 503 | `DEPENDENCY_UNAVAILABLE` | PASSED |
| Transaction failure | 500 | `INTERNAL_ERROR` | PASSED |

## 4. Structured Logging Evidence

The application produces structured JSON logs containing:

- `timestamp`
- `level`
- `correlation_id`
- `operation`
- `outcome`
- `duration_ms`

Example from the test execution:

```json
{
  "level": "ERROR",
  "correlation_id": "2016caf5-8e2d-451e-9b25-cf61f0796d95",
  "operation": "POST /complaints",
  "outcome": "error",
  "duration_ms": 5.39
}
```

The full log entry, including its timestamp, is preserved in the test output file.

## 5. Transaction Safety

The integration test `test_rollback_when_status_event_fails` simulates an error during status-history event insertion.

The API returns HTTP 500 with the standardized error code `INTERNAL_ERROR`.

The test verifies that the complaint is not persisted when the associated history event cannot be inserted.

**Result: PASSED**

## 6. Conclusion

The tested failure scenarios returned the expected HTTP responses and standardized API error codes.

Structured error logs provide request traceability through correlation IDs and operation metadata.

The tests confirm transaction rollback behavior for the simulated event-insertion failure.

Authentication and authorization remain a separately documented security limitation.