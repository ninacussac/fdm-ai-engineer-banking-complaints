import chromadb
import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "gemini").lower()

if EMBEDDING_PROVIDER =="ollama":
    CHROMA_PATH=os.getenv("OLLAMA_CHROMA_PATH", "data/chroma_ollama")
    COLLECTION_NAME = "banking_policy_chunks_nomic"

elif EMBEDDING_PROVIDER == "gemini":
    CHROMA_PATH = os.getenv("CHROMA_PATH", "data/chroma_embedding")
    COLLECTION_NAME = "banking_policy_chunks"
else:
    raise ValueError(f"Unsupported embedding supporter : {EMBEDDING_PROVIDER}")


# Create persistent ChromaDB client
chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

# Create or retrieve collection
collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=None,
    configuration={"hnsw": {"space": "cosine"}}
)

def get_stored_ids():
    results = collection.get(include=[])
    return results["ids"]

def store_embeddings(chunks):
    collection.upsert(
        ids=[chunk["chunk_id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        embeddings=[chunk["embedding"] for chunk in chunks],
        metadatas=[
            {
                "chunk_id": chunk["chunk_id"],
                "source_id": chunk["source_id"],
                "title": chunk["title"],
                "section_title": chunk["section_title"],
                "document_type": chunk["document_type"],
                "effective_version": chunk["version"],
                "effective_date": chunk["effective_date"],
                "access_label": chunk["access_label"],
                "status": chunk["status"]
            }
            for chunk in chunks
        ]
    )

def count_vectors():
    return collection.count()

def get_all_vectors():
    return collection.get(
        include=["embeddings", "metadatas"])

def search_vectors(query_embedding, top_k=3, filters=None):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=filters
    )