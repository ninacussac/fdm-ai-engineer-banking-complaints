# Week 4 — Clean Setup Test

## Objective

Verify that a developer who did not implement the project can set up and run the application by following the README.

## Test Environment

- **Tester:** Pending
- **Operating system:** Pending
- **Python version:** 3.12
- **Git branch:** feature/week4-release
- **Test date:** Pending

## Setup Checklist

- [ ] Clone the repository
- [ ] Create and activate a virtual environment
- [ ] Install dependencies using `requirements.txt`
- [ ] Configure `.env` using `.env.example`
- [ ] Obtain the authorized policy corpus
- [ ] Run document ingestion
- [ ] Run chunking and embedding generation
- [ ] Start FastAPI
- [ ] Query `POST /policy/query`
- [ ] Run automated tests

## Known Issues Identified During Preparation

### Issue 1 — Missing RAG Dependencies

**Problem:** `requirements.txt` did not include ChromaDB, Google GenAI or python-docx.

**Action:** Added the missing dependencies.

**Verification:** Pending clean installation.

### Issue 2 — Incomplete Environment Configuration

**Problem:** `.env.example` did not include the RAG environment variables.

**Action:** Added `GOOGLE_API_KEY`, `EMBEDDING_MODEL`, `GENERATION_MODEL` and `CHROMA_PATH`.

**Verification:** Pending independent setup.

### Issue 3 — Policy Corpus Not Tracked in Git

**Problem:** The policy documents are not included in the repository.

**Action:** Documented the authorized corpus installation process in the README.

**Verification:** Pending access by an independent tester.

## Test Result

**Status:** Not yet executed.

## Additional Defects

None recorded yet.