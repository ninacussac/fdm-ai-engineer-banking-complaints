# Embedding Pipeline — Operational Notes

## 1. Configuration

- **Provider:** Google Gemini
- **Embedding model:** gemini-embedding-2
- **Vector database:** ChromaDB
- **Batch size:** 32 chunks
- **Embedding dimensions:** 3072
- **Input dataset:** `data/processed/chunks_selected.jsonl`
- **Total chunks:** 208

## 2. Execution Results

| Execution | Chunks processed | Duration |
|---|---:|---:|
| First storage run | 64 | 37.26 seconds |
| Second storage run | 144 | 145.41 seconds |
| **Total** | **208** | **182.67 seconds** |

The pipeline generates embeddings in batches and stores each successfully processed batch immediately in ChromaDB.

Existing chunk IDs are checked before embedding generation to prevent duplicate processing.

A repeated execution with 64 previously stored chunks completed in 0.03 seconds without generating new embeddings.

## 3. Error Handling

During development, the Gemini API returned an HTTP 429 `RESOURCE_EXHAUSTED` error due to free-tier rate limits.

The pipeline implements:
- Retry attempts for failed embedding batches.
- Delays between batches to reduce API rate-limit errors.
- Immediate persistence of successfully processed batches.
- Automatic skipping of previously stored chunk IDs when execution resumes.

These mechanisms allow the pipeline to recover from interruptions without restarting the entire embedding process.

## 4. API Usage and Cost

- **API access:** Google Gemini free tier
- **Total embeddings stored:** 208
- **Measured processing duration:** 182.67 seconds
- **Token usage:** Not measured
- **Monetary cost:** Not independently measured

The recorded duration covers the two successful storage runs. It excludes earlier development tests and interruptions.

No precise API cost can be calculated from the available execution logs.

## 5. Vector Index Validation

The resulting ChromaDB index was validated against the selected chunks.

| Validation | Result |
|---|---|
| Expected chunks | 208 |
| Stored vectors | 208 |
| Embedding dimensions | 3072 |
| Invalid dimensions | 0 |
| Missing metadata | 0 |
| Duplicate IDs | 0 |
| Missing vectors | 0 |
| Unexpected vectors | 0 |
| **Overall status** | **PASS** |

The complete validation results are available in `vector_index_validation.json`.

## 6. Limitations

- API latency and throughput depend on Gemini quota limits and service availability.
- Fixed retry delays may not be optimal for every rate-limit error.
- The pipeline identifies previously stored chunks by ID; changes to the text or embedding model require rebuilding the affected index.
- Exact token consumption and monetary cost were not measured.