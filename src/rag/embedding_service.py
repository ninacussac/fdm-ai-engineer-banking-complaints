import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
import time
from src.rag.vector_store import store_embeddings, count_vectors, get_stored_ids
# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

# Create Gemini client
client = genai.Client(api_key=GOOGLE_API_KEY)

def load_chunks(file_path):
    chunks = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            chunks.append(json.loads(line))

    return chunks

def get_gemini_embedding(text):
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    return response.embeddings[0].values

def embed_batch(chunks):
    # creer les batch pour que cela renvoie bien 32
    # differents embedding et pas juste un pour 32 chunks
    contents=[
        types.Content(parts=[types.Part(text=chunk["text"])])
                      for chunk in chunks
    ]
    #pour chaque chunk cree un contenu compris par gemini

    response = client.models.embed_content(
        model = EMBEDDING_MODEL,
        contents=contents
    )
    #item => type ContentEmbedding and item.value => numerical vector
    embeddings = [item.values for item in response.embeddings]

    if (len(embeddings)!=len(chunks)):
        raise ValueError("Embedding count does not match chunk count")

    return embeddings



def generate_embeddings(chunks, batch_size=32):
    # Skip chunks already stored in ChromaDB
    existing_ids = set(get_stored_ids())

    remaining_chunks = [
        chunk for chunk in chunks
        if chunk["chunk_id"] not in existing_ids
    ]

    print("Chunks remaining:", len(remaining_chunks))

    for i in range(0, len(remaining_chunks), batch_size):
        batch = remaining_chunks[i:i + batch_size]

        for attempt in range(3):
            try:
                embeddings = embed_batch(batch)

                results = []

                for chunk, embedding in zip(batch, embeddings):
                    results.append({
                        **chunk, # donne toutes les infos contenues dans chunk
                        "embedding": embedding
                    })

                # Save this batch immediately
                store_embeddings(results)

                print(f"Batch {i // batch_size + 1} stored")
                break

            except Exception as error:
                print(f"Error: {error}")

                if attempt == 2:
                    raise
                # limitation gemini 100 query/minute
                if "429" in str(error):
                    time.sleep(35)
                else:
                    time.sleep(2)

        # Reduce the risk of reaching the API rate limit
        if i + batch_size < len(remaining_chunks):
            time.sleep(35)

    print("Total vectors stored:", count_vectors())


if __name__ == "__main__":
    chunks = load_chunks("data/processed/chunks_selected.jsonl")

    start = time.time()

    generate_embeddings(chunks, batch_size=32)

    duration = time.time() - start
    print("Duration:", round(duration, 2), "seconds")