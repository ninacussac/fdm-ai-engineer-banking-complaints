# RAG Evaluation — Baseline Report

## 1. Objective

The objective of Exercise 4.4.2 is to establish a reproducible baseline for the banking policy RAG system.

The evaluation measures retrieval performance, answer support classification, citation quality, faithfulness, and abstention behavior.

The golden set was locked before running the baseline and was not modified based on the results.

## 2. Evaluation Setup

- **Dataset:** `evaluation/golden_set.csv`
- **Total cases:** 6
- **Supported cases:** 5
- **Unsupported cases:** 1
- **Retrieval configuration:** Top-k = 5, cosine similarity
- **Minimum similarity threshold for generation:** 0.70
- **Reranking:** Disabled
- **Evaluation method:** Automated checks and human review

The baseline was evaluated using the existing RAG pipeline without implementing improvements during the evaluation.

## 3. Baseline Results

| Metric | Result |
|---|---|
| Source Hit@5 | 100% (5/5) |
| Section Hit@5 | 80% (4/5) |
| Support Classification Accuracy | 83.33% (5/6) |
| Expected Citation Match | 40% (2/5) |
| Citation Validity | 100% (6/6) |
| Faithfulness | 100% (6/6) |
| Unsupported Question Abstention | 100% (1/1) |

Citation validity and faithfulness were assessed through human review of the six recorded responses.

The results describe only this small evaluation dataset and do not establish general system accuracy.

## 4. Case-Level Findings

| Case | Result | Main Finding |
|---|---|---|
| EV-001 | Pass | Expected intake policy retrieved and cited |
| EV-002 | Citation mismatch | Correct answer, but FAQ cited instead of expected policy section |
| EV-003 | Pass | Expected escalation section retrieved and cited |
| EV-004 | Citation mismatch | Answer supported by other retrieved evidence |
| EV-005 | Failure | Expected prohibition section not retrieved; incorrect abstention |
| EV-006 | Pass | Unsupported question correctly rejected |

## 5. Failure Analysis

Three cases require attention:

- **EV-002:** Citation selection favored a FAQ despite the expected policy section being available.
- **EV-004:** Citation selection favored historical cases and another policy section.
- **EV-005:** Retrieval failed to surface the expected section, leading to an incorrect abstention.

No unsupported factual claims were identified in the human review.

Detailed findings are documented in `evaluation/failure_analysis.md`.

## 6. Recommended Improvements

1. Investigate indexing and retrieval ranking for EV-005.
2. Evaluate prioritization of authoritative policy sources when choosing citations.
3. Review chunk boundaries for structured policy information.
4. Re-run the same locked golden set after improvements and compare against this baseline.

These improvements have not yet been implemented.

## 7. Acceptance Assessment

The baseline demonstrates strong source-level retrieval and correct abstention for the unsupported question.

However, section-level retrieval, expected citation matching, and supported-question coverage require improvement.

## 8. Limitations

- The golden set contains only six cases.
- Only one unsupported question was tested.
- Faithfulness was assessed manually.
- Expected citation matching is stricter than factual correctness.
- The results depend on the current document index, model behavior, and retrieval configuration.
- Generation results may vary between runs.

## 9. Conclusion

The baseline provides a reference point for future RAG improvements.

The main priorities are improving retrieval of specific policy sections and ensuring that generated citations select appropriate supporting evidence.

The locked golden set and original baseline results should be preserved for subsequent comparisons.