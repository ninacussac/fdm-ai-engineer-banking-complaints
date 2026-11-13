import os
import json
from dotenv import load_dotenv
from google import genai
from src.rag.retrieval_service import retrieve
from src.rag.citations import format_citations

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def build_prompt(question, evidence):
    prompt = f"""
    You are a banking policy assistant.

    Answer the question using ONLY the retrieved evidence below.

    Rules:
    1. Do not invent information.
    2. Keep the answer concise. 
    3. If evidence is insufficient, say you cannot answer.
    4. If only part of the question is supported, answer that part
    and explain what information is missing.
    5. Cite only chunk IDs present in the retrieved evidence.
    6. Return valid JSON with exactly these fields:
    answer, supported, citations, limitations.
    7. Try to use as much relevant chunks as possible.

    Use this JSON format:
    {{
        "answer": "Your answer",
        "supported": true,
        "citations": ["chunk_id"],
        "limitations": []
    }}

    Question:
    {question}

    Retrieved evidence:
    {evidence}
    """
    return prompt

def generate_answer(question, evidence):
    prompt = build_prompt(question, evidence)

    response = client.models.generate_content(
        model=os.getenv("GENERATION_MODEL"),
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )

    return json.loads(response.text)

MIN_SIMILARITY = 0.70
def answer_question(question, document_type=None, effective_version=None, access_label=None):
    # Retrieve relevant chunks
    chunks = retrieve(question, top_k=5,document_type=document_type, effective_version=effective_version, access_label=access_label)
    # Keep only sufficiently relevant chunks
    chunks = [
        chunk for chunk in chunks
        if chunk["score"] >= MIN_SIMILARITY
    ]
    # Return a safe response if no evidence is found
    if not chunks:
        return {
            "answer": "I could not find sufficient evidence.",
            "supported": False,
            "citations": [],
            "limitations": ["No supporting policy evidence found."]
        }

    # Prepare evidence for Gemini
    evidence = ""

    for chunk in chunks:
        evidence += f"""
        Chunk ID: {chunk["chunk_id"]}
        Source: {chunk["metadata"]["source_id"]}
        Section: {chunk["metadata"]["section_title"]}
        Text: {chunk["text"]}
        """

    # Generate the answer
    result = generate_answer(question, evidence)

    # Validate and format citations
    result["citations"] = format_citations(
        result["citations"],
        chunks
    )

    return result