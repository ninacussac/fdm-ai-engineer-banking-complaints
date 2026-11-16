import os
import json
from dotenv import load_dotenv
from google import genai
from src.rag.retrieval_service import retrieve
from src.rag.citations import format_citations
from ollama import Client as OllamaClient
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
    5. Citations must contain only exact chunk IDs copied
    character-for-character from the retrieved evidence.
    Never shorten, rewrite, or reconstruct a chunk ID.
    If no retrieved chunk directly supports the answer,
    do not cite it.
    6. Return valid JSON with exactly these fields:
    answer, supported, citations, limitations.
    7. Preserve exact conditions, numerical boundaries, exceptions,
    and requirements stated in the evidence.
    Do not generalize or modify them.

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

def generate_answer(question, evidence,chunks):
    prompt = build_prompt(question, evidence)
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    allowed_ids = [chunk["chunk_id"] for chunk in chunks]

    response_schema = {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "supported": {"type": "boolean"},
            "citations": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": allowed_ids
                }
            },
            "limitations": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": [
            "answer",
            "supported",
            "citations",
            "limitations"
        ],
        "additionalProperties": False
    }

    if provider =="gemini":
        response = client.models.generate_content(
            model=os.getenv("GENERATION_MODEL"),
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        result = json.loads(response.text)

    elif provider=="ollama":
        ollama_client = OllamaClient(
            host=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
        response = ollama_client.chat(model=os.getenv("OLLAMA_MODEL","llama3.2:1b"), 
                                      messages = [{"role":"system","content":("You are a banking policy assistant"
                                                                              "Return a valid JSON only.")},
                                                {"role":"user", "content":prompt}],
                                      format=response_schema,
                                      options={"temperature":0},
                                      think=False,)
        result = json.loads(response.message.content)

    else:
        raise ValueError(f"unsupported LLM provider:{provider}")

    required_fields = {
        "answer": str,
        "supported": bool,
        "citations": list,
        "limitations": list,
    }

    for field, expected_type in required_fields.items():
        if field not in result:
            raise ValueError(f"Missing response field : {field}")
        if not isinstance(result[field],expected_type):
            raise ValueError(f"Invalid type for field : {field}")

    return result

MIN_SIMILARITY = 0.70
def answer_question(question, document_type=None, effective_version=None, access_label=None):
    # Retrieve relevant chunks
    chunks = retrieve(question, top_k=10,document_type=document_type, effective_version=effective_version, access_label=access_label)
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
    result = generate_answer(question, evidence,chunks)

    try:
        result["citations"] = format_citations(
            result["citations"], chunks
        )

    except ValueError as error:
        return {
            "answer": "I could not produce a fully verified answer.",
            "supported": False,
            "citations": [],
            "limitations": [
                "The generated answer contained invalid citations."
            ]
        }

    return result