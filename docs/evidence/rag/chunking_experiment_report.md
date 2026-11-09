# Chunking Experiment

## Configurations

Two chunking strategies were implemented and evaluated using 175 normalized sections from the policy knowledge base.

### Baseline — Fixed-size chunking

The baseline strategy splits text into fixed-size chunks, regardless of paragraph or sentence boundaries.

- **Chunk size:** 500 characters
- **Overlap:** 50 characters
- **Generated chunks:** 208
- **Metadata:** Preserved for each chunk

This approach is simple and deterministic. However, it can split sentences, table rows, or related policy information across chunk boundaries.

### Structure-aware chunking

The structure-aware strategy prioritizes document structure when splitting text.

It groups paragraphs when possible and preserves line boundaries for long paragraphs, particularly those containing tables. If an individual line exceeds the maximum size, fixed-size splitting is used as a fallback.

- **Maximum chunk size:** 500 characters
- **Fallback overlap:** 50 characters
- **Generated chunks:** 208
- **Metadata:** Preserved for each chunk

Unlike the baseline, the structure-aware approach does not systematically apply overlap between chunks. Overlap is used only when splitting lines that exceed the size limit.

Both strategies produce deterministic chunk IDs and preserve document metadata, including source identifiers, section titles, versions and access labels.

## Locked queries

The three supplied queries from `tests/data/chunking_experiment_cases.json` were used without modification.

| Case ID | Query | Expected source | Expected section |
|---|---|---|---|
| CH-001 | When is supervisor approval required? | KB-002 | 3. Financial Redress Thresholds |
| CH-002 | What evidence is needed for a fee complaint? | KB-003 | 2. Required Intake Fields |
| CH-003 | When should suspected account takeover be escalated? | KB-004 | 4. Security Escalation Indicators |

## Retrieval evidence

### Chunk validation

Both strategies were validated for unique chunk IDs, source lineage, empty content and excessive chunk size.

| Validation metric | Baseline | Structure-aware |
|---|---:|---:|
| Total chunks | 208 | 208 |
| Duplicate IDs | 0 | 0 |
| Missing source information | 0 | 0 |
| Empty chunks | 0 | 0 |
| Chunks exceeding 500 characters | 0 | 0 |

All validation checks passed.

### Retrieval methodology

Retrieval was evaluated using **BM25**, a keyword-based ranking algorithm.

The search indexed document titles, section titles and chunk text. The same queries and retrieval settings were applied to both chunking strategies.

No embeddings or vector database were used in the final experiment.

For each query, the three highest-ranked chunks were retrieved. A test was considered successful only when at least one retrieved chunk matched both the expected source ID and section title.

### Retrieval results

| Case ID | Baseline Hit@3 | Structure-aware Hit@3 |
|---|---|---|
| CH-001 | Fail | Fail |
| CH-002 | Fail | Fail |
| CH-003 | Fail | Fail |
| **Total** | **0/3** | **0/3** |

Neither strategy retrieved the exact expected sections within the Top-3 results.

However, some retrieved chunks contained relevant information from alternative sections. Therefore, the results were also examined qualitatively.

## Failure analysis

### CH-001 — Supervisor approval

Both strategies retrieved `KB-009 — FAQ-005`, which directly answers the question about supervisor approval.

This FAQ states that supervisor approval is required when proposed compensation exceeds CAD 1,000 and explicitly references `KB-002 §3` as the authoritative source.

Although the retrieved information was relevant, the expected section itself was absent from the Top-3.

**Observation:** Strict source-section matching does not necessarily reflect whether retrieved information can answer the question.

### CH-002 — Fee complaint evidence

The expected section, `KB-003 — 2. Required Intake Fields`, contains the required information for a fee complaint, including fee type, amount, currency, date, account reference and previous contacts.

The baseline retrieved passages concerning approval rejection, general operational questions, and fee redress.

The structure-aware strategy retrieved similar general information, including complaint definitions.

Neither strategy returned the required intake fields in the Top-3.

**Observation:** BM25 ranked passages sharing vocabulary with the question above the section containing the required information.

### CH-003 — Account takeover escalation

The expected section was `KB-004 — 4. Security Escalation Indicators`.

The baseline retrieved general operational questions, complaint triage rules and resolution procedures.

The structure-aware strategy retrieved information about fraud specialist responsibilities and complaint triage.

These passages were partially relevant because they described how suspected fraud or identity compromise should be routed to human reviewers.

However, neither strategy retrieved the specific security escalation indicators from the expected section.

**Observation:** The retrieved chunks contained related operational guidance but lacked the complete evidence needed for the specific question.

### Chunk boundary analysis

Beyond retrieval ranking, the two strategies were compared for their ability to preserve related information.

The baseline strategy occasionally split sentences and table rows at arbitrary character positions.

For example, a FAQ answer about citation requirements was divided across chunks:

> How should evidence be cited? | Use stable structured-source references and

The structure-aware strategy preserved the complete question-answer row:

> How should evidence be cited? | Use stable structured-source references and current approved document source ID, version and section.

This illustrates an improvement in preserving meaningful units of information, although no improvement in exact-section Hit@3 was observed.

## Selected strategy

**Selected strategy: Structure-aware chunking**

**Configuration:**
- Maximum chunk size: 500 characters
- Fallback overlap: 50 characters
- Output: `data/processed/chunks_selected.jsonl`
- Total selected chunks: 208

The structure-aware strategy was selected because it better preserves paragraph boundaries and table rows while satisfying all validation requirements.

Both strategies achieved the same retrieval result of 0/3 using BM25. Therefore, the selection is based on the observed quality of chunk boundaries rather than a demonstrated improvement in retrieval performance.

The structure-aware strategy provides a more suitable foundation for the subsequent RAG pipeline because it reduces the risk of separating related information across chunks.

## Limitations

- **Limited evaluation set:** Only three queries were available, which limits the reliability of the comparison.
- **Keyword-based retrieval:** BM25 relies on lexical matches and may fail to identify relevant passages that use different terminology.
- **Strict success criteria:** Relevant alternative sources were counted as failures when they did not match the expected source and section.
- **Long text splitting:** Individual lines exceeding the maximum chunk size may still be split at arbitrary character positions.
- **Incomplete context preservation:** Structure-aware chunking does not guarantee that all related rules, conditions and exceptions remain together.
- **No semantic retrieval evaluation:** Embeddings and vector-based retrieval were excluded from this final experiment and can be evaluated in subsequent RAG exercises.

Overall, the experiment demonstrated that both strategies produce valid, traceable chunks, but neither achieved successful exact-section retrieval with BM25 on the supplied queries. Structure-aware chunking was selected for its observed improvements in preserving document structure and related information.