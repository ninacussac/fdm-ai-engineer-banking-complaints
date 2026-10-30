import argparse
import logging
import os
import sqlite3
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = PROJECT_ROOT / "data" / "database" / "database_schema.sql"
DB_PATH = PROJECT_ROOT / "data" / "database" / "seeded_test.db"
SEED_PATH = PROJECT_ROOT / "data" / "database" / "seed_data.sql"
LOG_PATH = PROJECT_ROOT / "seed_run_log.txt"
REPORT_PATH = PROJECT_ROOT / "integrity_report.txt"
EXPECTED_TABLE_COUNT = 16

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def load_seed_data(connection, seed_path):
    """
    Load SQL seed data into the current transaction.

    An error interrupts loading so the caller can rollback.
    """
    seed_path = Path(seed_path)

    if not seed_path.is_file():
        raise FileNotFoundError(
            f"Seed file not found: {seed_path}"
        )

    sql_content = seed_path.read_text(encoding="utf-8-sig")

    logger.info("Starting seed data loading.")

    statement = ""
    inserted_statements = 0

    for line in sql_content.splitlines(keepends=True):
        statement += line

        if sqlite3.complete_statement(statement):
            sql = statement.strip()

            if not sql or not any(
                part.strip() and not part.strip().startswith("--")
                for part in sql.splitlines()
            ):
                statement = ""
                continue

            # Execute inside the caller's transaction.
            connection.execute(sql)
            inserted_statements += 1
            statement = ""

    if statement.strip() and not statement.strip().startswith("--"):
        raise ValueError("Incomplete SQL statement in seed file.")

    logger.info(
        "Seed loading completed: %s INSERT statements executed.",
        inserted_statements
    )



def verify_integrity(connection):
    """
    Verify row counts, foreign keys, and account ownership.
    Return a formatted integrity report.
    """

    logger.info("Starting database integrity verification.")

    expected_counts = {
        "employee": 10,
        "customer": 10,
        "account": 10,
        "complaint": 30,
        "complaint_status_history": 30,
        "transactions": 10,
        "fee": 10,
        "service_request": 10,
        "policy_document": 10,
        "policy_section": 10,
        "investigation": 10,
        "recommendation": 10,
        "review_request": 10,
        "review_decision": 10,
        "customer_response": 10,
        "audit_log": 10,
    }

    report = [
        "DATABASE INTEGRITY REPORT",
        "=" * 45,
        "",
        "1. TABLE ROW COUNTS",
        "-" * 45,
    ]

    errors = []

    for table, expected in expected_counts.items():
        actual = connection.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        status = "PASS" if actual == expected else "FAIL"

        report.append(
            f"{table}: expected={expected}, "
            f"actual={actual} [{status}]"
        )

        if actual != expected:
            errors.append(
                f"{table}: expected {expected}, found {actual}"
            )

    report.extend([
        "",
        "2. FOREIGN KEY VALIDATION",
        "-" * 45,
    ])

    foreign_key_errors = connection.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()

    report.append(
        f"Foreign key violations: {len(foreign_key_errors)}"
    )

    if foreign_key_errors:
        errors.append(
            f"{len(foreign_key_errors)} foreign key violations"
        )

    report.extend([
        "",
        "3. COMPLAINT ACCOUNT OWNERSHIP",
        "-" * 45,
    ])

    mismatches = connection.execute("""
        SELECT c.complaint_id
        FROM complaint AS c
        JOIN account AS a
            ON c.account_id = a.account_id
        WHERE c.customer_id <> a.customer_id
    """).fetchall()

    report.append(
        f"Account ownership mismatches: {len(mismatches)}"
    )

    if mismatches:
        errors.append(
            f"{len(mismatches)} complaint account mismatches"
        )

    report.extend([
        "",
        "4. COMPLAINTS WITHOUT AN ACCOUNT",
        "-" * 45,
    ])

    missing_accounts = connection.execute("""
        SELECT complaint_id
        FROM complaint
        WHERE account_id IS NULL
        ORDER BY complaint_id
    """).fetchall()

    report.append(
        f"Complaints with NULL account_id: {len(missing_accounts)}"
    )

    for complaint in missing_accounts:
        report.append(f"  - {complaint[0]}")

    report.extend([
        "",
        "5. FINAL RESULT",
        "-" * 45,
    ])

    if errors:
        report.append("STATUS: FAIL")
        report.extend(errors)
        logger.error("Integrity verification failed: %s", errors)
    else:
        report.append("STATUS: PASS")
        logger.info("Integrity verification passed.")

    return "\n".join(report) + "\n", errors




def initialize_database(db_path: Path, schema_path: Path, reset: bool = False) -> None:
    """Create a fresh SQLite database; replace an existing one only with reset=True."""
    db_path = Path(db_path).resolve()
    schema_path = Path(schema_path).resolve()

    # Check is the sql file is found
    if not schema_path.is_file():
        raise FileNotFoundError(f"SQL schema not found: {schema_path}")
    
    # If database exists and no reset command an error is raised 
    if db_path.exists() and not reset:
        raise FileExistsError(
            f"Database already exists: {db_path}. Use --reset to recreate it."
        )

    
    sql_script = schema_path.read_text(encoding="utf-8-sig")
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Create in the same directory so replacement remains on one filesystem.
    fd, temporary_filename = tempfile.mkstemp(
        prefix="seed_temp_", suffix=".db", dir=db_path.parent
    )
    os.close(fd)
    temporary_path = Path(temporary_filename)

    logger.info("Initialization started; reset=%s; target=%s", reset, db_path)
    connection = None
    try:
        connection = sqlite3.connect(temporary_path)
        connection.execute("PRAGMA foreign_keys = ON")
        logger.info("Executing schema from %s", schema_path)        
        connection.executescript(sql_script)

        connection.execute("BEGIN")

        try:
            load_seed_data(connection, SEED_PATH)

            # Check foreign key constraints
            foreign_key_errors = connection.execute(
                "PRAGMA foreign_key_check"
            ).fetchall()

            if foreign_key_errors:
                raise RuntimeError(
                    f"Foreign key violations: {foreign_key_errors}"
                )

            # Verify that complaint accounts belong to their customers
            mismatched_accounts = connection.execute("""
                SELECT c.complaint_id
                FROM complaint AS c
                JOIN account AS a ON c.account_id = a.account_id
                WHERE c.customer_id <> a.customer_id
            """).fetchall()

            if mismatched_accounts:
                raise RuntimeError(
                    f"Complaint/customer account mismatches: "
                    f"{mismatched_accounts}"
                )

            connection.commit()
            logger.info("Seed transaction committed successfully.")

        except Exception:
            connection.rollback()
            logger.exception("Seed transaction rolled back.")
            raise


        tables = [
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' "
                "ORDER BY name"
            )
        ]
        logger.info("Schema created %d tables: %s", len(tables), ", ".join(tables))
        if len(tables) != EXPECTED_TABLE_COUNT:
            raise RuntimeError(
                f"Expected {EXPECTED_TABLE_COUNT} tables, found {len(tables)}."
            )

        integrity_result = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity_result != "ok":
            raise RuntimeError(f"SQLite integrity check failed: {integrity_result}")

        foreign_key_errors = connection.execute("PRAGMA foreign_key_check").fetchall()
        if foreign_key_errors:
            raise RuntimeError(f"Foreign key issues: {foreign_key_errors}")

        integrity_report, integrity_errors = verify_integrity(connection)

        if integrity_errors:
            raise RuntimeError(
            "Integrity verification failed. "
            "Database replacement cancelled."
        )
        connection.close()
        connection = None

        # Close SQLite3 Editor / DBeaver connections before running with --reset.
        os.replace(temporary_path, db_path)
        REPORT_PATH.write_text(integrity_report,encoding="utf-8")
        logger.info("Integrity report generated: %s",REPORT_PATH)
        
        logger.info("Initialization completed successfully: %s", db_path)
        print(f"Database initialized successfully ({len(tables)} tables): {db_path}")

    except Exception:
        logger.exception("Initialization failed; existing database was not intentionally replaced")
        raise
    finally:
        if connection is not None:
            connection.close()
        if temporary_path.exists():
            temporary_path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize the SQLite training database")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Explicitly permit replacement of an existing training database",
    )
    args = parser.parse_args()
    initialize_database(DB_PATH, SCHEMA_PATH, reset=args.reset)


if __name__ == "__main__":
    main()
