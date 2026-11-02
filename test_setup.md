# Integration Test Setup — Week 3

## 1. Objective

Test the FastAPI endpoints using a temporary SQLite database.

The integration tests verify HTTP responses, database persistence, error handling and transaction rollback.

## 2. Test Environment

- Python 3.12
- pytest
- FastAPI TestClient
- SQLAlchemy
- SQLite

## 3. Database Isolation

The `tests/integration/conftest.py` file contains reusable fixtures.

- `test_db` creates a temporary SQLite database using pytest's `tmp_path`.
- SQLAlchemy tables are created in the test database.
- A test customer (`CUS001`) and account (`ACC001`) are inserted before each test.
- `client` overrides FastAPI's `get_db` dependency to use the test database.
- Sessions and database connections are closed after each test.

The FastAPI lifespan configuration skips normal database table initialization while the application is in testing mode.

Tests are run sequentially because the testing flag and dependency overrides are shared application state.

## 4. Running Tests

Activate the Python virtual environment and execute:

```powershell
python -m pytest tests/integration -v
```

To generate the test report:

```powershell
python -m pytest tests/integration -v | Out-File -FilePath integration_test_report.txt -Encoding utf8
```

## 5. Covered Scenarios

- Customer lookup: HTTP 200 and 404.
- Complaint creation: HTTP 201.
- Request validation: HTTP 422.
- Valid complaint status update: HTTP 200.
- Invalid status transition: HTTP 409.
- Simulated database unavailability: HTTP 503.
- Transaction rollback when status event insertion fails: HTTP 500.
- Correlation ID consistency in error responses.
- Verification of persisted complaint data and status history.

## 6. Repeatability

The integration suite was executed twice successfully:

- Run 1: 10 passed in 0.72s.
- Run 2: 10 passed in 0.78s.

The same tests were also executed in reverse order:

- Reverse order: 10 passed in 0.74s.

These results provide evidence of repeatability and order independence for the tested execution orders.

## 7. Known Limitations

- Database unavailability is simulated by raising a SQLAlchemy `OperationalError`, rather than shutting down a real database.
- The test suite is designed for sequential execution.
- A full test of all possible execution orders has not been performed.
- These tests do not evaluate the future RAG functionality.