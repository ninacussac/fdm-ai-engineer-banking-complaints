# Fdm-ai-engineer-banking-complaints
AI-Powered Banking Complaint Assistant

## Data Access Layer

### 1. SQLite Configuration

The application uses SQLite for data persistence.

Database connections and transactions are managed through the `DatabaseManager` class.

Database paths are configured using environment variables stored in a `.env` file.

Two variables are defined:

- `DB_PATH`: Path to the main SQLite database.
- `DB_TEST_PATH`: Path to the SQLite test database.

Currently, `DatabaseManager` uses `DB_TEST_PATH` to ensure that database operations are performed on the test database.

The database manager is responsible for:

- Loading database configuration.
- Validating that the database file exists.
- Opening and closing database connections.
- Committing successful transactions.
- Rolling back failed transactions.
- Preventing multiple active connections on the same manager.

Example:

    from src.data import DatabaseManager

    db = DatabaseManager()
    connection = db.connect()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM complaint")
        results = cursor.fetchall()

    finally:
        db.close()

Database paths are resolved relative to the project root.

The `.env` file should not be committed to Git.

#### Dependencies

The DatabaseManager requires `python-dotenv` to load environment variables from the `.env` file.

Install the dependency using:

```bash
pip install python-dotenv
```

### 2. Repository Responsibilities

The application uses the Repository Pattern to separate database operations from application logic.

Each repository is responsible for accessing a specific type of data:

| Repository | Responsibility |
|---|---|
| CustomerRepository | Retrieve customer information |
| AccountRepository | Retrieve account information |
| ComplaintRepository | Retrieve and create complaints |

Repositories use the DatabaseManager to access SQLite and execute parameterized SQL queries.

This design improves code organization, reusability, and maintainability.

#### CustomerRepository

Provides access to customer information.

- `get_by_id(customer_id)`: Retrieves a customer by ID.
  Returns a dictionary if found, otherwise `None`.

#### AccountRepository

Provides access to customer accounts.

- `get_for_customer(customer_id)`: Retrieves all accounts
  associated with a customer.
  Returns a list of dictionaries or an empty list.

#### ComplaintRepository

Handles complaint retrieval and creation.

- `get_by_id(complaint_id)`: Retrieves a complaint by ID.
  Returns a dictionary or `None`.

- `get_for_customer(customer_id)`: Retrieves all complaints
  associated with a customer.
  Returns a list of dictionaries or an empty list.

- `create(...)`: Creates a new complaint in the database.
  Generates a complaint ID, commits the transaction on success,
  and rolls back if an SQLite error occurs.
  Returns no value.

All repositories use parameterized SQL queries and rely on DatabaseManager for connection handling.

### 3. Repository Usage Examples

#### Retrieve a customer

```python
from src.data import DatabaseManager
from src.data.customer_repository import CustomerRepository

db = DatabaseManager()
customer_repo = CustomerRepository(db)

customer = customer_repo.get_by_id("CUS001")

if customer:
    print(customer)
```

#### Retrieve customer accounts

```python
from src.data.account_repository import AccountRepository

account_repo = AccountRepository(db)

accounts = account_repo.get_for_customer("CUS001")

for account in accounts:
    print(account)
```

#### Retrieve a complaint

```python
from src.data.complaint_repository import ComplaintRepository

complaint_repo = ComplaintRepository(db)

complaint = complaint_repo.get_by_id("CMP001")

if complaint:
    print(complaint)
```

#### Retrieve customer complaints

```python
complaints = complaint_repo.get_for_customer("CUS001")

for complaint in complaints:
    print(complaint)
```

#### Create a new complaint

```python
complaint_repo.create(
    customer_id="CUS001",
    category="Fee Dispute",
    channel="Email",
    status="OPEN",
    received_at="2026-10-27 14:00:00",
    complaint_text="Incorrect account fee charged.",
    priority="Medium",
    account_id="ACC001"
)
```

The create() method generates a complaint ID with the CP prefix and a five-digit number, based on the highest existing complaint ID.

The method commits successful insertions and rolls back transactions when an SQLite error occurs.

It does not return a value.

### 4. SQL Query Boundaries

SQL queries are centralized within the repository layer.

#### Allowed

- Repository classes can execute SQL queries.
- Repositories use parameterized queries to prevent SQL injection.
- DatabaseManager handles connections and transactions.
- Repository tests may execute SQL queries to verify results.

#### Not Allowed

- Business logic should not contain direct SQL queries.
- Application services should not independently manage database connections.

This architecture separates data access from business logic, improves maintainability, and makes repositories easier to test.

### 5. Testing

Repository tests verify:
- Successful retrieval of existing records.
- Handling of missing records.
- Successful complaint creation.
- Rejection of invalid insertions.

Run the complaint repository tests from the project root:

```bash
python -m tests.test_complaint_repository
```

Repository tests use the SQLite database configured through DB_TEST_PATH, keeping test operations separate from the main database configured through DB_PATH. Tests that modify data should use disposable test fixtures to ensure repeatability.


---

## Week 3 — FastAPI Complaint API

### Overview

The Week 3 implementation introduces a REST API built with FastAPI to manage banking complaints, customers, accounts, and complaint status history.

The application follows a layered architecture:

**API Routers → Service Layer → Repository Layer → SQLite Database**

FastAPI handles HTTP requests, Pydantic validates request data, the service layer implements business rules, and SQLAlchemy repositories manage database persistence.

### Setup

From the project root, create and activate a Python virtual environment.

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

Configure the required environment variables using `.env.example` as a reference.

For detailed database setup instructions, see the [Setup Guide](docs/setup/README_setup.md).

### Running the API

Start the FastAPI development server from the project root:

```bash
python -m uvicorn src.main:app --reload
```

The API is available by default at:

- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

### Available API Resources

| Resource | Endpoint | Description |
|---|---|---|
| Complaints | `POST /complaints` | Create a complaint |
| Complaints | `GET /complaints` | Retrieve complaints |
| Complaints | `GET /complaints/{complaint_id}` | Retrieve a specific complaint |
| Complaints | `PATCH /complaints/{complaint_id}/status` | Update complaint status |
| Customers | `/customers` | Access customer information |
| Accounts | `/accounts` | Access account information |
| Events | `GET /events` | Retrieve complaint status history |
| Health | `/health`, `/health/live`, `/health/ready` | Application health checks |

The complete API contract is available in [openapi.json](openapi.json).

### Testing

The project uses pytest for unit and integration testing.

Run unit tests:

```bash
python -m pytest tests/unit -v
```

Run integration tests:

```bash
python -m pytest tests/integration -v
```

Run the complete test suite:

```bash
python -m pytest tests/unit tests/integration -v
```

**Week 3 release validation results:**

- Unit tests: 31 passed
- Integration tests: 13 passed
- Total: 44 passed

Integration tests use a temporary SQLite database to isolate test operations.

### Error Handling and Logging

The API implements standardized error responses using `AppError` and structured request logging.

Error responses include an error code, a safe message, and a correlation ID for traceability.

The logging middleware records request operations, outcomes, processing duration, and correlation IDs.

### Week 3 Release Evidence

- [Architecture Diagram](docs/architecture/week3_architecture.md)
- [End-to-End Test Report](docs/evidence/week3_release/end_to_end_report.md)
- [Unit Test Report](docs/evidence/week3_release/unit_test_report.txt)
- [Integration Test Report](docs/evidence/week3_release/integration_test_report.txt)
- [Error Handling and Logging Evidence](docs/evidence/week3_release/error_logging_evidence.md)
- [Detailed Logging Test Output](docs/evidence/week3_release/error_logging_test_output.txt)
- [OpenAPI Specification](openapi.json)

### Known Limitations

The current API does not enforce authentication or role-based authorization.

This limitation was identified during the Week 3 code review and requires remediation or an explicitly approved deferral before the application is deployed with real customer data.

The Week 3 release serves as the API baseline for the Week 4 RAG implementation.