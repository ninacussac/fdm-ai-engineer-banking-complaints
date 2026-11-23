# Sprint 2 — Demo Script

## 1. Objective

Demonstrate the Week 3 Complaint API and the Week 4 RAG Policy Knowledge Service.

The demonstration covers:

- Complaint API functionality.
- Supported policy questions with citations.
- Filtered policy retrieval.
- Unsupported questions and abstention.
- RAG evaluation baseline results.

## 2. Prerequisites

- Python virtual environment activated.
- Dependencies installed.
- `.env` configured with the Gemini API key.
- SQLite test database available.
- Policy documents ingested and indexed in ChromaDB.

## 3. Start the Application

From the project root:

```powershell
python -m uvicorn src.main:app --reload
```

Open the Swagger interface:

`http://127.0.0.1:8000/docs`

## 4. Demo Scenario — Filtered Policy Question

**Endpoint:** `POST /policy/query`

**Request:**

```json
{
  "question": "What triggers immediate specialist escalation?",
  "document_type": "Policy",
  "effective_version": "2.1",
  "access_label": "Restricted"
}
```

**Expected behavior:**

- HTTP 200.
- `supported = true`.
- A grounded answer about specialist escalation.
- Citation to `KB-002`, section `4. Specialist Escalation Triggers`.
- No citations outside the permitted retrieval filters.

**Observed result:** HTTP 200, supported answer and matching citation during the local Swagger test.

**Security note:** These filters are technical retrieval filters, not authorization controls. Production access to Restricted documents must be enforced by the server.

## 5. Demo Scenario — Supported Policy Question

**Objective:** Demonstrate that the RAG service retrieves relevant policy evidence and generates a grounded answer with citations.

**Endpoint:** `POST /policy/query`

**Request:**

```json
{
  "question": "What triggers immediate specialist escalation?"
}
```

**Expected behavior:**

- HTTP 200.
- `supported = true`.
- The answer identifies relevant specialist escalation triggers.
- The response contains citations to retrieved policy evidence.

**Previously observed result:**

- `supported = true`.
- The answer identified unauthorized transactions, stolen cards, identity compromise and possible personal-data exposure.
- Citation: `KB-002`, section `4. Specialist Escalation Triggers`, version `2.1`.

**Evidence:** `evidence/week4/answer_generation_test.json`

During the demo, verify that the answer remains grounded in the returned citations.

## 6. Demo Scenario — Unsupported Policy Question

**Objective:** Demonstrate that the RAG service abstains when no sufficient policy evidence is available.

**Endpoint:** `POST /policy/query`

**Request:**

```json
{
  "question": "What is the current weather in Reykjavik?"
}
```

**Expected behavior:**

- HTTP 200.
- `supported = false`.
- An answer indicating insufficient evidence.
- An empty `citations` list.
- A limitation explaining that no supporting policy evidence was found.

**Previously observed result:**

```json
{
  "answer": "I could not find sufficient evidence.",
  "supported": false,
  "citations": [],
  "limitations": [
    "No supporting policy evidence found."
  ]
}
```

**Evidence:** `evidence/week4/abstention_test.json`

This result was recorded during Exercise 4.4.2. It does not represent a new live API test.

During the demo, verify that the service does not generate unsupported information or fabricated citations.

## 7. Demo Scenario — Complaint API

**Objective:** Demonstrate that the Week 3 Complaint API remains functional after integrating the Week 4 RAG service.

**Endpoint:** `GET /complaints`

**Steps:**

1. Start FastAPI.
2. Open `http://127.0.0.1:8000/docs`.
3. Find `GET /complaints`.
4. Click **Try it out**.
5. Click **Execute**.

**Expected behavior:**

- HTTP 200.
- The API returns the complaints available in the configured SQLite database.
- The request does not modify complaint data.

**Verification:**

Check the HTTP response status and returned data.

**Regression evidence:** `evidence/week4/regression_tests.txt`

The automated regression suite passed 92 tests during Week 4 release preparation.


## 8. RAG Evaluation Results

**Objective:** Present the Week 4 RAG evaluation baseline and explain the main findings.

The evaluation uses six questions: five supported and one unsupported.

| Metric | Result |
|---|---|
| Source Hit@5 | 100% (5/5) |
| Section Hit@5 | 80% (4/5) |
| Support Classification Accuracy | 83.33% (5/6) |
| Expected Citation Match | 40% (2/5) |
| Citation Validity | 100% (6/6) |
| Faithfulness | 100% (6/6) |
| Unsupported Question Abstention | 100% (1/1) |

**Main findings:**

- EV-002 and EV-004 returned grounded answers but did not cite the expected policy sections.
- EV-005 failed to retrieve the expected section and incorrectly abstained.
- EV-006 correctly abstained for an unsupported question.

**Evaluation report:** `evaluation/evaluation_report.md`

**Failure analysis:** `evaluation/failure_analysis.md`

These results describe the original six-case baseline. They do not establish production readiness.

## 9. Demo Summary

The demonstration covers:

- Week 3 Complaint API: `GET /complaints` returned HTTP 200 and complaint records.
- Week 4 grounded answer generation with citations.
- Policy retrieval using document type, version and access-label filters.
- Abstention when sufficient policy evidence is unavailable.
- Baseline retrieval and answer evaluation metrics.

**Known limitations:**

- Gemini may occasionally return HTTP 503 due to temporary service unavailability.
- Retrieval did not identify the expected section for every supported question.
- Citation matching requires improvement.
- Access-label filtering is not a replacement for server-side authorization.

## 10. Conclusion

The Week 4 RAG service is integrated with the existing Complaint API.

The recorded tests demonstrate core API and RAG functionality. The identified limitations remain documented for future improvements and Sprint 3 handover.