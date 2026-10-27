# Database Initialization and Seeding — Setup Guide

## 1. Overview

This utility initializes and populates a local SQLite database for the Banking Complaint Resolution System (CRS) project.

The script automatically:

- Creates the database using the provided SQL schema.
- Creates and verifies the 16 database tables.
- Loads synthetic banking data from SQL seed files.
- Enforces foreign key constraints.
- Uses a transaction to prevent partial data insertion.
- Validates record counts and complaint/account relationships.
- Generates execution logs and an integrity report.
- Supports controlled database reset using the `--reset` option.

## 2. Prerequisites

Before running the utility, ensure that:

- Python 3 is installed.
- The project repository has been cloned locally.
- The SQL schema and seed files are available.
- The terminal is opened at the project root.

SQLite support is included in Python through the built-in `sqlite3` module.

No additional Python packages are required for the seeding script.

## 3. Required Files

| File | Purpose |
|---|---|
| `scripts/seed_database.py` | Database initialization, data loading, and validation |
| `data/database/database_schema.sql` | SQL statements defining the 16 database tables |
| `data/database/seed_data.sql` | Synthetic data used to populate the database |
| `data/database/seeded_test.db` | Generated SQLite database |
| `seed_run_log.txt` | Execution history and error logs |
| `integrity_report.txt` | Database integrity verification results |

The database file and reports are generated or updated when the script executes successfully.

## 4. Repository Environment Configuration

The database repositories use environment variables to locate the SQLite database.

1. Initialize the database using `python -m scripts.seed_database`.
2. Install the required dependency using `pip install python-dotenv`.
3. Copy `.env.example` to `.env`.
4. Verify that `DB_TEST_PATH` points to the generated SQLite database.
5. Run a repository retrieval test:

```bash
python -c "from src.data import DatabaseManager; from src.data.customer_repository import CustomerRepository; print(CustomerRepository(DatabaseManager()).get_by_id('CUS001'))"
```

The expected result is a dictionary containing customer `CUS001`.

The `.env` file must not be committed to Git. Repository tests that modify records should use a separate disposable SQLite database.

## 5. Initial Database Setup

From the project root, execute:

```bash
python -m scripts.seed_database
```

If the database does not already exist, the script will:

1. Validate the schema file.
2. Create a temporary SQLite database.
3. Execute the schema.
4. Load the synthetic data.
5. Validate database integrity.
6. Create the final database file.
7. Generate the integrity report and logs.

Expected output:

```text
Database initialized successfully (16 tables): ...
```

## 6. Reset an Existing Database

If the database already exists, running the initialization command without `--reset` raises a `FileExistsError`.

This prevents accidental database replacement.

To explicitly recreate the database, execute:

```bash
python -m scripts.seed_database --reset
```

**Warning:** A successful reset replaces the existing database and removes its previous contents.

The utility builds and validates a temporary database before replacing the target database. If schema execution, data insertion, or integrity validation fails, the existing database is not intentionally replaced.

Close any applications or editor connections using the SQLite database before resetting it.

This utility is intended for local development and testing environments, not production databases.

## 7. Seed Data

The project uses SQL seed scripts supplied for the FDM training exercise.

The original SQL seed file was supplemented with additional complaint records.

Expected dataset:

| Table | Expected Rows |
|---|---:|
| employee | 10 |
| customer | 10 |
| account | 10 |
| complaint | 30 |
| complaint_status_history | 30 |
| transactions | 10 |
| fee | 10 |
| service_request | 10 |
| policy_document | 10 |
| policy_section | 10 |
| investigation | 10 |
| recommendation | 10 |
| review_request | 10 |
| review_decision | 10 |
| customer_response | 10 |
| audit_log | 10 |

Three complaints intentionally contain a NULL `account_id`: `CMP023`, `CMP029`, and `CMP030`.

These are valid records because complaints can exist without a linked bank account.

## 8. Data Validation and Transaction Management

The utility enables SQLite foreign key enforcement using:

```sql
PRAGMA foreign_keys = ON;
```

Seed insertions are executed inside a transaction.

If an insertion fails, the transaction is rolled back.

The integrity verification checks:

- Actual versus expected table row counts.
- Foreign key violations.
- Complaint/account ownership consistency.
- Complaints without an associated account.
- SQLite database integrity.

Any critical validation failure prevents replacement of the existing database.

## 9. Verify Successful Initialization

After execution, inspect:

```text
integrity_report.txt
```

A successful run should end with:

```text
STATUS: PASS
```

You can also verify the database manually using a SQLite editor:

```sql
SELECT COUNT(*) AS total_complaints
FROM complaint;
```

Expected result:

```text
30
```

To verify foreign key consistency:

```sql
PRAGMA foreign_key_check;
```

Expected result: no returned rows.

## 10. Logging

The script records initialization events in:

```text
seed_run_log.txt
```

Logs include:

- Initialization start.
- Schema execution.
- Seed data loading.
- Transaction commit or rollback.
- Integrity verification.
- Initialization completion or failure.

Errors are recorded with traceback details to assist troubleshooting.

## 11. Troubleshooting

**FileExistsError — Database already exists**

The target database already exists.

Use `--reset` only when replacement is intended.

**FileNotFoundError — SQL schema or seed file missing**

Verify that `database_schema.sql` and `seed_data.sql` exist in `data/database/`.

**sqlite3.IntegrityError — FOREIGN KEY constraint failed**

A record references another record that does not exist, or a required relationship is invalid.

Review the SQL data and execution logs.

**sqlite3.OperationalError — Database is locked**

Close SQLite editors or other applications holding an active database connection, then retry.

**Integrity verification failed**

Inspect `seed_run_log.txt` and check the seed data for unexpected record counts or inconsistent references.

## 12. Testing and Known Limitations

The following scenarios have been tested:

- Successful database initialization.
- Protection against accidental reset.
- Explicit database reconstruction.
- Successful insertion of synthetic data.
- Rollback following a foreign key constraint violation.
- Database integrity verification.

The original exercise describes validation and loading from CSV files. However, the supplied data used in this implementation was provided as SQL INSERT statements.

Therefore, the implementation validates SQL insertion integrity rather than CSV headers. SQL errors are logged, but individual rejected CSV rows are not tracked.

Expected record counts are based on the provided synthetic dataset and must be updated if the source data changes.

## 13. Reuse in Future Exercises

The generated SQLite database can be reused for repository tests, SQL queries, complaint analysis, and later Banking CRS development exercises.

The seeding utility provides a repeatable local test environment without requiring manual database setup.