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