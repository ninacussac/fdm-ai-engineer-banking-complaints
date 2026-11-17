# Fdm-ai-engineer-banking-complaints
AI-Powered Banking Complaint Assistant
## Installation and Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd fdm-ai-engineer-banking-complaints
```

### 2. Create a Virtual Environment

The project uses Python 3.12.

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example configuration:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace `your_google_api_key_here` with a valid Google Gemini API key.

The configuration includes:

- `DB_PATH` and `DB_TEST_PATH`: SQLite database paths.
- `DATABASE_URL`: SQLAlchemy database connection.
- `GOOGLE_API_KEY`: Gemini API authentication.
- `EMBEDDING_MODEL`: Model used to generate embeddings.
- `GENERATION_MODEL`: Model used to generate grounded answers.
- `CHROMA_PATH`: ChromaDB storage directory.

Do not commit `.env` or share your API key.

### 5. Verify the Installation

Run the existing tests from the project root:

```powershell
python -m pytest tests/ -v
```

The Week 4 release preparation recorded 92 passing tests. Test results may change as the project evolves.

## Running the API

Start the FastAPI application from the project root:

```powershell
python -m uvicorn src.main:app --reload
```

The API runs locally at:

`http://127.0.0.1:8000`

Open the interactive API documentation:

`http://127.0.0.1:8000/docs`

The application includes complaint management endpoints and the policy knowledge service.

The RAG endpoint is:

`POST /policy/query`

Example request:

```json
{
  "question": "What triggers immediate specialist escalation?"
}
```

The response contains the generated answer, a support indicator, citations and limitations.

Stop the server using `Ctrl+C`.

## RAG Document Ingestion

The RAG pipeline processes approved banking policy documents and stores their embeddings in ChromaDB.

### 1. Prepare Policy Documents

The policy document corpus is provided separately from the Git repository.

To run ingestion, obtain the approved Week 4 policy corpus through the authorized FDM distribution channel.

Extract the files into `docs/policies/`, preserving the original folder structure.

Ensure the manifest exists at:

`docs/policies/05_Manifests_and_Guides/knowledge_base_manifest.csv`

The manifest contains document metadata and relative paths required by the ingestion service.

Documents marked as `Superseded` are excluded from ingestion. Documents not listed in the manifest are rejected.

Do not commit Internal or Restricted policy documents unless explicitly authorized.

### 2. Extract Documents

From the project root, run:

```powershell
python -m src.rag.ingestion_service
```

This validates the manifest, extracts the DOCX content and generates:

`data/processed/documents.jsonl`

It also creates `ingestion_run_log.json`.

### 3. Create Chunks

```powershell
python -m src.rag.chunking
```

This creates the baseline and structure-aware chunks.

The selected chunks are saved to:

`data/processed/chunks_selected.jsonl`

### 4. Generate Embeddings and Populate ChromaDB

```powershell
python -m src.rag.embedding_service
```

This reads the selected chunks, generates embeddings using Gemini and stores them in ChromaDB.

Chunks with IDs already present in the vector store are skipped.

An internet connection and a valid `GOOGLE_API_KEY` are required.

### 5. Verify the Vector Store

```powershell
python -c "from src.rag.vector_store import count_vectors; print('Stored vectors:', count_vectors())"
```

A successful ingestion should produce a non-zero vector count.

During Week 4 release preparation, the existing vector store contained 208 vectors.

**Note:** Re-running the ingestion and chunking scripts overwrites their generated JSONL files. The embedding script skips existing chunk IDs, so changes to chunk content may require rebuilding the index in a separate environment.

## RAG Querying and Evaluation

### 1. Query the Policy Knowledge Service

Start the API:

```powershell
python -m uvicorn src.main:app --reload
```

Open the interactive API documentation:

`http://127.0.0.1:8000/docs`

Find the `POST /policy/query` endpoint and select **Try it out**.

Example request:

```json
{
  "question": "What triggers immediate specialist escalation?"
}
```

The response includes:

- `answer`: Generated answer based on retrieved policy evidence.
- `supported`: Indicates whether sufficient evidence was found.
- `citations`: References to the supporting policy documents.
- `limitations`: Information that could not be established.

### 2. Run Automated Tests

From the project root:

```powershell
python -m pytest tests/ -v
```

### 3. Review the RAG Evaluation Baseline

The Week 4 evaluation artifacts are stored in `evaluation/`:

- `golden_set.csv`: Locked evaluation questions and expected references.
- `baseline_results.csv`: Retrieval and answer evaluation results.
- `evaluation_report.md`: Baseline metrics and conclusions.
- `failure_analysis.md`: Identified failures and proposed improvements.
- `answer_results.json`: Recorded generated answers.

The baseline contains six cases: five supported questions and one unsupported question.

Key baseline results:

| Metric | Result |
|---|---|
| Source Hit@5 | 100% |
| Section Hit@5 | 80% |
| Support Classification Accuracy | 83.33% |
| Expected Citation Match | 40% |

The original baseline should be preserved for comparison with future improvements.

### 4. Review Week 4 Test Evidence

Test evidence is available in `evidence/week4/`.

It includes regression tests, ingestion tests, an example grounded answer and a recorded abstention.

The recorded abstention comes from the previous evaluation baseline and is not a new live generation test.

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