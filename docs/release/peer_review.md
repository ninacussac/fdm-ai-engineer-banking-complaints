# Week 2 — Data Foundation Peer Review

## 1. Review Information

- **Project:** Banking Complaint Resolution System (CRS)
- **Exercise:** 2.5.2 — Review and Release the Week 2 Data Foundation
- **Author:** Nina Cussac
- **Reviewer:** Pending assignment
- **Review status:** In progress
- **Scope:** Week 2 deliverables, Exercises 2.1.1–2.5.1

## 2. Review Checklist

| ID | Review Criterion | Status | Evidence |
|---|---|---|---|
| REV-01 | Database schema builds successfully | PASS | 16 tables created during Exercise 2.5.1 |
| REV-02 | Database seeding succeeds | PASS | SQL seed script executed successfully with 30 complaints |
| REV-03 | Database integrity checks pass | PASS | `integrity_report.txt` reports PASS, with zero foreign key violations |
| REV-04 | SQL query files execute successfully | PARTIAL | Corrected JOIN and repeat-complainant queries were run successfully; full execution of all Week 2 SQL files remains pending |
| REV-05 | Python analysis matches expected results | PASS (output comparison) | Complaint counts, percentages and average resolution times match between the summary and exported CSV. Independent execution pending |
| REV-06 | Repositories use parameterized SQL | PASS (static review) | All three repositories use bound SQL parameters. Complaint creation and invalid-customer rejection tests passed; complete regression testing remains pending |
| REV-07 | README references real files and commands | PENDING VERIFICATION | README examples and setup instructions reportedly corrected (FIND-012, FIND-013); modified files and clean setup have not yet been independently verified |

## 3. Findings

### FIND-001 — SQL Seeding Instead of CSV Validation

- **Severity:** To be agreed with reviewer
- **Area:** Database seeding
- **Description:** The seeding utility uses the SQL INSERT scripts supplied for the project instead of the CSV loading process described in Exercise 2.5.1.
- **Evidence:** `data/database/seed_data.sql`, `scripts/seed_database.py`
- **Impact:** CSV header validation and individual CSV-row rejection reporting are not implemented.
- **Action:** Confirm acceptance of SQL-based seeding with the coach or implement the missing CSV-specific requirements.
- **Status:** Open

---

### FIND-002 — Week 2 Deliverables Not Consolidated

- **Severity:** High
- **Area:** Release readiness / Repository structure
- **Description:** Several Week 2 deliverables are distributed across separate feature branches and are not currently included in the Week 2 release branch.
- **Evidence:** git diff --name-status HEAD against the Week 2 SQL, personas, and Python analysis branches.
- **Impact:** A developer checking out the current release branch cannot access all required Week 2 artifacts. The release is therefore not yet independently reproducible.
- **Action:** Consolidate the required reviewed artifacts into the release baseline while preserving existing database components and avoiding unrelated or duplicate files.
- **Status:** Open — blocking release.

---

### FIND-003 — Missing `date_closed` Column in Database Schema

- **Severity:** High
- **Area:** SQL Queries / Database Schema
- **Description:** Requirement 7 asks to identify closed complaints where `date_closed` is missing. However, the current `complaint` table does not contain a `date_closed` column. The existing query uses `complaint_status_history.changed_at`, which represents the timestamp of a status change rather than the complaint's actual closure date.
- **Evidence:** `data/database/queries/basic_queries.sql` (Query 7) and `data/database/database_schema.sql`.
- **Impact:** The query cannot fully satisfy Requirement 7 or reliably identify closed complaints with missing closure dates.
- **Owner:** Nina Cussac
- **Proposed Action:** Clarify the expected closure-date field with the coach. Either update the database schema to include `date_closed` or execute the validation against a dataset containing that field.
- **Status:** Open — awaiting clarification.

---

### FIND-004 — High-Priority Complaint Definition Requires Clarification

- **Severity:** Low
- **Area:** SQL Queries / Business Logic
- **Description:** Requirement 2 asks to list high-priority unresolved complaints. The current query filters only records where `priority = 'High'`, while the dataset also contains complaints with `priority = 'Critical'`. It is unclear whether critical complaints should also be included in the high-priority category.
- **Evidence:** `data/database/queries/basic_queries.sql` (Query 2) and `data/database/seed_data.sql`.
- **Impact:** If critical complaints are considered high-priority, the current query excludes relevant unresolved complaints and underreports the number of high-priority cases.
- **Owner:** Nina Cussac
- **Proposed Action:** Confirm the business definition of high-priority complaints. If both `High` and `Critical` should be included, update the filter to `priority IN ('High', 'Critical')`.
- **Status:** Open — awaiting clarification.

---

### FIND-005 — JOIN Queries Table Name Compatibility

- **Severity:** High
- **Area:** SQL Queries / Database Schema Compatibility
- **Description:** JOIN queries used plural table names inconsistent with the current SQLite schema.
- **Evidence:** `data/database/queries/join_queries.sql`; seeded SQLite database.
- **Owner:** Nina Cussac
- **Correction:** Changed `complaints`, `customers`, and `accounts` to `complaint`, `customer`, and `account`.
- **Validation:** Executed corrected JOIN queries and checked complaint preservation, including NULL account links.
- **Result:** PASS — 30 rows, 30 distinct complaints, including three complaints without a linked account.
- **Status:** Resolved — pending reviewer approval.
- **Commit reference:** Pending.

---

### FIND-006 — View Creation Is Not Idempotent

- **Severity:** Low
- **Area:** SQL Views / Reproducibility
- **Description:** The `complaint_analyst_view.sql` script uses `CREATE VIEW` without checking whether the view already exists.
- **Evidence:** `data/database/queries/complaint_analyst_view.sql`.
- **Impact:** Re-executing the script on an existing database raises an error because the view has already been created.
- **Owner:** Nina Cussac
- **Proposed Action:** Use `CREATE VIEW IF NOT EXISTS` for repeatable creation, or explicitly drop and recreate the view when its definition changes.
- **Status:** Open — non-blocking.

---

### FIND-007 — Repeat Complainant Count

- **Severity:** Medium
- **Area:** Advanced SQL / CTE and Window Functions
- **Description:** The previous query used a non-aggregated rank as a proxy for complaint count.
- **Evidence:** `data/database/queries/advanced_queries.sql` and executed query results.
- **Owner:** Nina Cussac
- **Correction:** Count complaints by `customer_id` using `COUNT(*)` and `GROUP BY` in a CTE.
- **Validation:** Executed the updated query on the 30-complaint seeded database.
- **Result:** PASS — 10 repeat complainants with a combined 30 complaints; all counts exceed one.
- **Status:** Resolved — pending reviewer approval.
- **Commit reference:** Pending.

---

### FIND-008 — Different Date Fields Across CSV and SQLite Sources

- **Severity:** Low
- **Area:** Python / Documentation / Data Contracts
- **Description:** The Python analysis expects `date_opened` and `date_closed` fields from the CSV dataset, while the SQLite schema uses `received_at` and does not provide a dedicated closure-date column.
- **Evidence:** `src/complaint_analysis.py` and `data/database/database_schema.sql`.
- **Impact:** Developers may incorrectly assume that the Python analysis can be executed directly against the seeded SQLite database without data transformation.
- **Owner:** Nina Cussac
- **Proposed Action:** Document the distinction between the CSV analysis dataset and the SQLite database schema, including their date-field mappings and limitations.
- **Status:** Open — documentation improvement.

---

### FIND-009 — AccountRepository Uses an Incorrect Table Name

- **Severity:** High
- **Area:** Python / Database Repositories
- **Description:** `AccountRepository.get_for_customer()` queried `accounts` instead of `account`.
- **Evidence:** `src/data/account_repository.py` and SQLite schema.
- **Owner:** Nina Cussac
- **Correction:** Changed the query to the singular `account` table, retaining SQL parameter binding.
- **Validation:** Local `get_for_customer("CUS001")` repository test reported as completed.
- **Result:** Expected account retrieval was reported successful; terminal output not attached to this review.
- **Status:** Resolved locally — pending reproducible regression test and reviewer approval.
- **Commit reference:** Pending.

---

### FIND-010 — ComplaintRepository Create Method

- **Severity:** High
- **Area:** Python / Database Repositories
- **Description:** The old INSERT used nonexistent `date_opened`, repeated `priority`, and omitted required `complaint_text`.
- **Evidence:** `src/data/complaint_repository.py`, SQLite schema and `tests/test_complaint_repository.py`.
- **Owner:** Nina Cussac
- **Correction:** Aligned the INSERT with `received_at`, `complaint_text`, and other schema columns; removed duplicate `priority`. Enabled SQLite foreign keys on connections.
- **Validation:** `python -m tests.test_complaint_repository`.
- **Result:** PASS — created and retrieved `CMP031`; invalid customer insertion was rejected. No independent post-failure row-count check has been recorded.
- **Status:** Resolved for tested scenarios — pending complete regression tests and reviewer approval.
- **Commit reference:** Pending.

---

### FIND-011 — Complaint ID Generation

- **Severity:** Medium
- **Area:** Python / Database Repositories
- **Description:** Generated `CP00001`-style IDs were incompatible with the seed format `CMP001`.
- **Evidence:** `src/data/complaint_repository.py` and seed records.
- **Owner:** Nina Cussac
- **Correction:** Standardized the generated prefix and numbering to `CMP###`.
- **Validation:** `python -m tests.test_complaint_repository`.
- **Result:** PASS — generated `CMP031` after the 30 seeded complaints.
- **Remaining issue:** `MAX + 1` is not safe for concurrent complaint creation.
- **Status:** Partially resolved — concurrency issue deferred for reviewer decision.
- **Commit reference:** Pending.

---

### FIND-012 — README Repository Examples Do Not Match Seeded Data

- **Severity:** Medium
- **Area:** Documentation / Repository Usage
- **Description:** The repository examples in `README.md` use customer and complaint identifiers (`C0079`, `CP00026`) that do not exist in the current seeded SQLite dataset. The complaint creation example also uses parameters that are not aligned with the current schema.
- **Evidence:** `README.md`, `data/database/seed_data.sql`, and `src/data/complaint_repository.py`.
- **Impact:** Developers following the README may receive empty query results or encounter errors when attempting to create complaints.
- **Owner:** Nina Cussac
- **Proposed Action:** Update the examples to use seeded identifiers such as `CUS001` and `CMP001`. Align the complaint creation example with the corrected repository interface.
- **Status:** Correction reported complete — pending README example verification and reviewer approval.

---

### FIND-013 — Missing End-to-End Database Configuration Instructions

- **Severity:** Medium
- **Area:** Documentation / Environment Setup
- **Description:** `README_setup.md` documents database initialization but does not explain how to configure the `DB_TEST_PATH` environment variable required by `DatabaseManager`. The `.env` configuration is referenced in `README.md`, but a complete setup procedure connecting the generated database to the repositories is missing.
- **Evidence:** `README.md`, `README_setup.md`, and `src/data/database_manager.py`.
- **Impact:** Another developer may successfully initialize the SQLite database but be unable to execute repository operations without additional configuration instructions.
- **Owner:** Nina Cussac
- **Proposed Action:** Add a `.env.example` file, document the required database environment variables, and include an end-to-end repository setup and verification example.
- **Status:** Instructions and `.env.example` reportedly added — pending clean setup verification.

## 4. Defect Tracking

For each additional finding, record:

- Finding ID
- Description
- Severity (Critical / High / Medium / Low)
- Evidence or reproduction steps
- Owner
- Proposed corrective action
- Resolution status
- Associated commit or PR

## 5. Resolution Evidence

| Finding | Changed file(s) | Validation evidence | Result | Fix commit |
|---|---|---|---|---|
| FIND-005 | `data/database/queries/join_queries.sql` | Ran updated JOINs; 30 distinct complaints and three NULL-account complaints preserved | PASS | Pending |
| FIND-007 | `data/database/queries/advanced_queries.sql` | Executed repeat-complainant CTE; 10 customers, total count 30 | PASS | Pending |
| FIND-009 | `src/data/account_repository.py` | Tested `get_for_customer("CUS001")` locally; capture complete test output for reproducibility | Reported PASS | Pending |
| FIND-010 | `src/data/complaint_repository.py`, `src/data/database_manager.py`, `tests/test_complaint_repository.py` | `python -m tests.test_complaint_repository`; `CMP031` created/retrieved, invalid customer rejected | PASS for tested scenarios | Pending |
| FIND-011 | `src/data/complaint_repository.py` | Created `CMP031` on a 30-complaint seed | PASS for ID format; concurrency not verified | Pending |
| FIND-012 | `README.md` | Author reports updated seeded IDs and complaint creation example | Pending verification | Pending |
| FIND-013 | `README_setup.md`, `.env.example` | Author reports documented setup and environment configuration | Pending independent clean setup | Pending |

All correction commits and PR references must be added after version control changes. Reported tests do not replace an independent clean setup by a non-author.

## 6. Deferred Issues

- **FIND-011 (concurrency):** The `MAX + 1` complaint ID algorithm may collide during simultaneous inserts. Defer only if the reviewer accepts strictly sequential local test use; otherwise fix before release.
- **FIND-006 (view idempotence):** Open low-severity improvement; review whether repeatable view creation is required for clean setup.
- **FIND-008 (CSV/SQLite date fields):** Document the distinct input data contracts before treating it as resolved.
- **FIND-001, FIND-003, FIND-004:** Await reviewer/coach decisions; not automatically approved for deferral.
- **FIND-002:** Remains a release blocker until the complete Week 2 baseline is integrated and verified.

## 7. Final Review Decision

**Status: PENDING**

Release approval requires completed checks, resolution of agreed blocking findings, and independent setup verification.

**Peer reviewer approval:** Pending