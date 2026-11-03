# Week 2 — Data Foundation Release Notes

**Project:** Banking Complaint Resolution System (CRS)  
**Exercise:** 2.5.2 — Review and Release the Week 2 Data Foundation  
**Candidate branch:** `feature/week2-release-integration`  
**Release status:** **Candidate — reviewer approval and independent verification pending**  
**Release tag:** Not created

## 1. Scope

- SQLite schema with 16 tables, initialized through `scripts/seed_database.py` using `data/database/database_schema.sql` and `data/database/seed_data.sql`.
- Synthetic seed dataset: 30 complaints, including three without an associated account (`CMP023`, `CMP029`, `CMP030`).
- SQL scripts for basic exploration, JOIN operations, complaint metrics, advanced SQL, and the analyst view.
- Python data-access layer (`DatabaseManager`, `CustomerRepository`, `AccountRepository`, `ComplaintRepository`) with parameterized SQL.
- CSV-based complaint analysis script and recorded outputs; the CSV analysis dataset (120 complaints) is distinct from the seeded SQLite dataset (30 complaints).
- Documentation, complaint journeys, personas, and associated user stories.

## 2. Validation evidence

- Clean-clone SQLite initialization: **PASS** — all 16 tables created and seeded.
- Integrity report: **PASS** — no foreign-key violations or complaint/account ownership mismatches; three expected NULL account IDs.
- Representative SQL in clean clone: **PASS** — 30 complaints total, 19 open, three without account, and 30 preserved by customer/account JOIN.
- Repository reads in clean clone: **PASS** — `CUS001` retrieved, one linked account, four linked complaints.
- Complaint creation testing on development test data: **PASS for tested scenarios** — `CMP031` created and retrieved; invalid customer insert rejected.
- Python analysis report/export comparison: **PASS for consistency of existing outputs**, not an independently reproduced run.
- Python analysis from clean Windows clone: **BLOCKED** by enterprise Code Integrity policy (events 3033/3077) refusing pandas `strptime.cp312-win_amd64.pyd`.

## 3. Known issues and limitations

- Python analysis cannot be reproduced on the tested Windows workstation until an approved environment is available.
- `src/complaint_analysis.py` expects `data/complaints.csv`, which was absent from the clean Git checkout; a shareable synthetic input or documented generation method is required for full reproducibility.
- `requirements.txt` was absent and pandas was not documented in the setup instructions at the time of the clean check.
- The database does not contain a dedicated `date_closed` field; the requirement to check closed complaints missing this field needs clarification.
- Business interpretation of `High` versus `Critical` priority remains subject to reviewer confirmation.
- Complaint ID generation based on `MAX + 1` is not concurrency-safe.
- Additional findings and their status are tracked in `docs/release/peer_review.md` (including any deferred metric or SQL issues).

## 4. Week 3 interfaces and assumptions

- SQLite tables: `customer`, `account`, `complaint`, and `complaint_status_history` are core sources for customer and complaint access.
- Complaint API operations should use the repositories, parameterized SQL, and `DatabaseManager` transaction handling.
- The current complaint creation interface accepts customer, category, channel, status, `received_at`, `complaint_text`, priority, and optional account ID.
- CSV analysis fields and SQLite fields are not interchangeable without explicit mapping and reconciliation.

## 5. Rebuild and recovery

1. Clone or check out the approved integration commit.
2. Follow `README_setup.md` to install dependencies, configure `.env` from `.env.example`, and run `python -m scripts.seed_database`.
3. Inspect `integrity_report.txt` and run representative SQL/repository checks.
4. To replace a **disposable local test database only**, close connections and run `python -m scripts.seed_database --reset`.
5. For rollback after a release, check out the last reviewer-approved tag or commit and rebuild a disposable database from its schema and seed; back up any database containing non-synthetic changes before replacing it.
