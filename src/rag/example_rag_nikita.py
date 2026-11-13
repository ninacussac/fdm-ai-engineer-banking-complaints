# ===================================================
from email.mime import text
from fileinput import filename
import os #Imports Python's operating system module.
import time #Used for delays
from dotenv import load_dotenv #Loads environment variables from a .env file
import chromadb #Imports Chroma vector database
from google import genai #Imports Google's new Gemini SDK.
# ==========================================================
# Load Environment Variables
# ==========================================================
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# ==========================================================
# Gemini Client
# ==========================================================
client = genai.Client(api_key=GOOGLE_API_KEY)
# ==========================================================
# ChromaDB Setup
# ==========================================================
chroma_client = chromadb.PersistentClient(
path="chroma_persistent_storage"
)
collection = chroma_client.get_or_create_collection(
name="document_qa_collection"
)
# ==========================================================
# Load Documents
# ==========================================================
def load_documents_from_directory(directory_path):
    print("==== Loading Documents ====")
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:
                documents.append(
                    {
                        "id": filename,
                        "text": file.read()
                    }
                )
    return documents

# ==========================================================
# Text Chunking
# ==========================================================
def split_text(text,chunk_size=1000,chunk_overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks

# ==========================================================
# Gemini Embeddings
# ==========================================================
def get_gemini_embedding(text):
    response = client.models.embed_content(
    model="models/gemini-embedding-2",
    contents=text)
    return response.embeddings[0].values

# ==========================================================
# Load and Chunk Documents
# ==========================================================
# Resolve data path relative to this script so execution works from any cwd.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
directory_path = os.path.join(BASE_DIR, "news_articles")
print("Current Directory:", os.getcwd())
print("Directory Exists:", os.path.exists(directory_path))
print(os.listdir(directory_path))
print("Contents of news_articles:")
print(os.listdir(directory_path))
documents = load_documents_from_directory(directory_path)
print(f"Loaded {len(documents)} documents")
chunked_documents = []
for doc in documents:
    chunks = split_text(doc["text"])
    for i, chunk in enumerate(chunks):
        chunked_documents.append(
            {
            "id": f"{doc['id']}_chunk{i+1}",
            "text": chunk
            }
        )
print("=====================Created chunks======================")
print(
f"Created {len(chunked_documents)} chunks"
)
print(chunked_documents)
# ==========================================================
# Generate Embeddings
# ==========================================================
print("==== Generating Embeddings ====")
for doc in chunked_documents:
    doc["embedding"] = get_gemini_embedding(doc["text"])
# ==========================================================
# Store in Chroma
# ==========================================================
print("==== Storing in Chroma ====")
collection.upsert(
    ids=[
        doc["id"]
        for doc in chunked_documents
    ],
    documents=[
        doc["text"]
        for doc in chunked_documents
    ],
    embeddings=[
        doc["embedding"]
        for doc in chunked_documents
    ]
)
print("==== Documents Stored ====")
# ==========================================================
# Retrieval Function
# ==========================================================
def query_documents(question,n_results=2):
    print("==== Querying Chroma ====")
    question_embedding = get_gemini_embedding(question)
    # print("Question embedding ",question_embedding)
    results = collection.query(query_embeddings=[question_embedding],n_results=n_results)
    # print(results)
    relevant_chunks = []
    for chunk_list in results["documents"]:
        relevant_chunks.extend(chunk_list)
    return relevant_chunks

# ==========================================================
# Gemini Response Generation
# ==========================================================
def generate_response(question,relevant_chunks):
    context = "".join(relevant_chunks)
    prompt = f"""
    You are a helpful assistant.
    Use the supplied context to answer
    the question.
    If the answer is not found in the
    context, say you don't know.
    Keep the answer concise.
    Context:{context}
    Question:{question}"""
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            response = client.models.generate_content(model="gemini-3.1-flash-lite",contents=prompt)
            return response.text
        except Exception as exc:
            error_text = str(exc)
            is_retryable = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text.lower())
            if not is_retryable or attempt == max_attempts:
                return (
                    "I could not generate an answer right now because the "
                    "Gemini API is temporarily unavailable. Please try again "
                    "in a few moments."
                    f"Technical details: {exc}"
                )
            wait_seconds = 2 ** attempt
            print(
            f"Gemini temporarily unavailable (attempt {attempt}/{max_attempts}). "
            f"Retrying in {wait_seconds}s..."
            )
            time.sleep(wait_seconds)

# ==========================================================
# Ask Question
# ==========================================================
question = "Tell me about Databricks"
question = "What is Spring boot"
relevant_chunks = query_documents(question,n_results=1)
print("==== Retrieved Chunks ====")
print(relevant_chunks)
for chunk in relevant_chunks:
    print(chunk[:200])
    print("-----------------")
answer = generate_response(question,relevant_chunks)
print("==== Final Answer ====")
print(answer)