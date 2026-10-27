# Week 2 — Independent Clean Setup Verification

**Project:** Banking Complaint Resolution System (CRS)  
**Candidate branch:** `feature/week2-release-integration`  
**Executor of checks below:** Project author (clean-clone rehearsal)  
**Independent reviewer:** Pending  
**Overall result:** **PARTIAL / BLOCKED — independent sign-off pending**

## Verification record

| ID | Check | Observed result | Status |
|---|---|---|---|
| SETUP-01 | Clone repository | Fresh branch clone used for tests | PASS (author rehearsal) |
| SETUP-02 | Install dependencies | Python and pandas installed; pandas cannot be loaded due to Windows policy | PARTIAL |
| SETUP-03 | Initialize SQLite | 16 tables created | PASS |
| SETUP-04 | Seed synthetic records | 30 complaints and expected seed table counts | PASS |
| SETUP-05 | Integrity report | STATUS: PASS, 0 FK violations, 0 ownership mismatches, 3 expected NULL account IDs | PASS |
| SETUP-06 | Representative SQL | 30 total complaints, 19 open, 3 without account, JOIN count 30 | PASS |
| SETUP-07 | Repository reads | CUS001 found; 1 account; 4 complaints | PASS (read operations only) |
| SETUP-08 | Python complaint analysis | Import of pandas fails before script executes | BLOCKED |
| SETUP-09 | README and tracked-file audit | Database docs/files present; analysis input and dependency instructions incomplete | FAIL / follow-up needed |

## SETUP-08 — Reproduction blocker

Command: `\.venv\Scripts\python.exe -m src.complaint_analysis`  
Python: 3.12.10; pandas: 3.1.0.

`ImportError: DLL load failed while importing strptime: Application control policy blocked this file.`

Imports fail in both system Python and the virtual environment. Windows Code Integrity events **3033** and **3077** identify blocked native module `pandas\_libs\tslibs\strptime.cp312-win_amd64.pyd`, policy ID `0283ac0f-fff1-49ae-ada1-8a933130cad6`. Resolution requires an approved execution environment or assistance from IT; do not disable enterprise safeguards.

## SETUP-09 — Documentation and file audit

The fresh clone contained the README files, `.env.example`, seeder, SQLite schema/seed, SQL queries, and repository modules, all tracked by Git.

Outstanding issues at audit time:
- `data/complaints.csv` was absent and untracked, although `src/complaint_analysis.py` depends on it.
- `requirements.txt` was absent; README documented `python-dotenv` but not `pandas`.
- Local `.venv/` was untracked; seeding modified `seed_run_log.txt` and `.env.example` showed a local modification. Keep generated/local configuration out of release commits.

## Independent reviewer execution

The independent reviewer must perform a fresh checkout using only the documentation, record the tested **commit SHA**, execute the database and Python checks in an approved environment, and note any remaining discrepancies here. The author's rehearsal does not satisfy the independent sign-off requirement.

**Reviewer name:** Pending  
**Reviewed commit:** Pending  
**Independent verdict:** Pending  
**Approval date:** Pending
