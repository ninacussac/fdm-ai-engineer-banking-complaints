# RAG Baseline — Failure Analysis

## 1. Overview

This document analyzes the failures identified during Exercise 4.4.2.

The evaluation uses six locked cases: five supported questions and one unsupported question.

## 2. Failure Taxonomy

The following categories are considered:

- **Ingestion:** Missing, outdated, or incorrectly ingested documents.
- **Chunking:** Relevant information is split or missing from the indexed chunks.
- **Retrieval:** The expected document or section is not retrieved.
- **Generation:** The generated answer or its citations do not match the expected behavior.
- **Labelling:** Expected labels or reference definitions require clarification.

## 3. Identified Failures

### EV-002 — Supervisor Approval

**Category:** Generation / Citation selection

**Expected:** KB-002, section 3. Financial Redress Thresholds.

**Observed:** The expected section was retrieved at rank 3 with a similarity score of 0.750 and passed the 0.70 threshold. However, Gemini cited KB-009 FAQ-005 instead.

**Impact:** Expected citation mismatch. The answer remained faithful to the evidence.

**Potential cause:** The FAQ provides a direct answer and was ranked above the authoritative policy section.

### EV-004 — Fee Refund

**Category:** Generation / Citation selection

**Expected:** KB-003, section 5. Redress and Approval.

**Observed:** The expected section was retrieved at rank 3 with a similarity score of 0.720 and passed the threshold. However, Gemini cited KB-003 section 3 and KB-010 historical cases.

**Impact:** Expected citation mismatch. The answer remained supported by the cited evidence.

**Potential cause:** The model selected passages containing more explicit wording about not promising redress.

### EV-005 — Authentication Secrets

**Category:** Retrieval

**Expected:** KB-004, section 5. Prohibited Behaviors.

**Observed:** The expected section was absent from the top five chunks. Only KB-004 section 3 passed the similarity threshold.

**Impact:** The system returned `supported=false` although the golden set expected a supported answer.

**Potential cause:** The retrieval ranking did not surface the relevant prohibition.

## 4. Cases Without Observed Failures

- **EV-001:** Expected source and section retrieved and cited; faithful answer.
- **EV-003:** Expected source and section retrieved and cited; faithful answer.
- **EV-006:** Unsupported question; correct abstention without citations.

## 6. Proposed Improvement Actions

### Action 1 — Improve Retrieval for EV-005

**Problem:** The expected section, KB-004 section 5, was not retrieved in the top five results.

**Proposed improvement:**
- Verify that the expected section is correctly indexed in ChromaDB.
- If indexed, investigate retrieval ranking and test keyword reranking or a larger candidate set.

**Success criterion:** KB-004 section 5 appears in the top five retrieved results.

### Action 2 — Improve Citation Selection for EV-002 and EV-004

**Problem:** Gemini cited FAQs or historical cases instead of the expected policy sections.

**Proposed improvement:**
- Investigate prioritizing authoritative policy documents when multiple sources support the same answer.
- Ensure citations remain grounded in the retrieved evidence.

**Success criterion:** The expected policy sections are cited without reducing answer faithfulness.

### Action 3 — Review Chunking Strategy

**Problem:** Relevant policy information may be split across multiple chunks, especially in structured tables.

**Proposed improvement:**
- Review chunk boundaries.
- Keep related rules, thresholds and exceptions together when possible.

**Success criterion:** Relevant policy evidence remains complete and retrievable.

### Action 4 — Re-run the Evaluation

After implementing improvements:

1. Keep the golden set unchanged.
2. Run the same six evaluation cases.
3. Compare the new results with the original baseline.
4. Document improvements and regressions.
5. Preserve the original baseline for comparison.

## 7. Improvement Priorities

| Priority | Action | Related Cases |
|---|---|---|
| High | Investigate retrieval ranking | EV-005 |
| Medium | Improve citation selection | EV-002, EV-004 |
| Medium | Review chunking boundaries | Potential cross-cutting issue |
| High | Re-run the locked evaluation | All cases |

These improvements are proposals only and were not implemented during the baseline evaluation.