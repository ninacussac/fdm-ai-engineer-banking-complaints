from src.rag.embedding_service import get_gemini_embedding
from src.rag.vector_store import search_vectors

def retrieve(query, top_k=3, document_type=None, effective_version=None, access_label=None, rerank=False):
    # Check the query
    if not query.strip():
        raise ValueError("Query cannot be empty")

    if top_k < 1:
        raise ValueError("top_k must be positive")

    filters = []

    if document_type:
        filters.append({"document_type": document_type})

    if effective_version:
        filters.append({"effective_version": effective_version})

    if access_label:
        filters.append({"access_label": access_label})

    # Combine filters
    if len(filters) == 0:
        where = None
    elif len(filters) == 1:
        where = filters[0]
    else:
        where = {"$and": filters}

    # Convert the question into an embedding
    query_embedding = get_gemini_embedding(query)

    # Search ChromaDB
    try:
        results = search_vectors(query_embedding, top_k, filters=where)
    except Exception as error:
        raise RuntimeError("Retrieval Service Unavailable") from error

    # Format the results
    retrieved_chunks = []

    for i in range(len(results["ids"][0])):
        distance = results["distances"][0][i]

        retrieved_chunks.append({
            "chunk_id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "score": 1 - distance,
            "metadata": results["metadatas"][0][i]
        })

    if rerank:
        retrieved_chunks = rerank_results(query, retrieved_chunks)

    return retrieved_chunks


def rerank_results(query, results):
    query_words = set(query.lower().split())

    for result in results:
        text_words = set(result["text"].lower().split())
        result["rerank_score"] = len(query_words & text_words)

    return sorted(results,key=lambda result: result["rerank_score"], reverse=True)