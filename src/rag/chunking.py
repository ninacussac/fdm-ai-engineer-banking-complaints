import json
from pathlib import Path
import re
from rank_bm25 import BM25Okapi

INPUT_PATH = Path("data/processed/documents.jsonl")
CASES_PATH = Path("tests/data/chunking_experiment_cases.json")

# queries
def load_experiment_cases():
    with open(CASES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

#KB documents
def load_documents():
    with open(INPUT_PATH, "r",encoding="utf-8") as file:
        return [json.loads(line) for line in file] # Load each line as a JSON object

#first method : fixed_chunk size
def fixed_chunk(text, chunk_size=500, overlap=50):
    chunks=[]

    if chunk_size<0 or overlap<0 or overlap>=chunk_size:
        raise ValueError("Invalid chunk size or overlap")
    
    step = chunk_size - overlap

    for start in range(0,len(text),step):
        chunk = text[start:start+chunk_size]
        if chunk:
            chunks.append(chunk)
        if start+chunk_size>=len(text):
            break
    return chunks


def create_baseline_chunks(documents, chunk_size=500, overlap=50):
    all_chunks =[]

    for document in documents:
        #Join section paragraph into one text
        text = "\n".join(document["content"])
        chunks = fixed_chunk(text, chunk_size, overlap)

        for index, chunk_text in enumerate(chunks, start=1):
            chunk = document.copy()
            chunk["chunk_id"]= (f"{document['chunk_id']}#baseline#{index:04d}")
            chunk["text"]=chunk_text
            chunk["content"]=[chunk_text]
            all_chunks.append(chunk)
    return all_chunks


def save_chunks(chunks, output_path):
    output_path=Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True) # Create the output directory if it doesn't exist

    with open(output_path,"w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk,ensure_ascii=False)+"\n")


def split_long_paragraph(paragraph, chunk_size=500, overlap=50):
    lines = paragraph.splitlines()
    chunks = []
    current_chunk = ""

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # A single line is too long
        if len(line) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            chunks.extend(
                fixed_chunk(line, chunk_size=chunk_size, overlap=overlap)
            )
            continue

        # The next line does not fit
        if current_chunk and len(current_chunk) + len(line) + 1 > chunk_size:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            if current_chunk:
                current_chunk += "\n" + line
            else:
                current_chunk = line

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

### More aware practice : ,

def structure_aware_chunk(paragraphs, chunk_size=500, overlap=50):
    chunks=[]
    current_chunk=""
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if len(paragraph) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            chunks.extend(
                split_long_paragraph(paragraph, chunk_size=chunk_size, overlap=overlap)
            )
            continue
          
        if current_chunk and len(current_chunk)+len(paragraph)+1>chunk_size:
            chunks.append(current_chunk)
            current_chunk=paragraph
        else:
            if current_chunk:
                current_chunk+= "\n" + paragraph
            else:
                current_chunk=paragraph
    
    if current_chunk:
        chunks.append(current_chunk)

    return chunks   


def create_structure_aware_chunks(documents,chunk_size=500, overlap=50):
    all_chunks=[]

    for document in documents:
        chunks = structure_aware_chunk(document["content"], chunk_size=chunk_size, overlap=overlap)

        for index,chunk_text in enumerate(chunks, start=1):
            chunk = document.copy()
            chunk["chunk_id"]=(f"{document['chunk_id']}#structure#{index:04d}")
            chunk["text"]=chunk_text
            chunk["content"]=[chunk_text]
            all_chunks.append(chunk)
    return all_chunks


def validate_chunks(chunks, max_size=500):
    ids = [chunk["chunk_id"] for chunk in chunks]

    duplicate_ids = len(ids)-len(set(ids))

    missing_source = sum(not chunk.get("source_id") or not chunk.get("section_title") 
                         for chunk in chunks)

    empty_chunks = sum(not chunk.get("text", "").strip() for chunk in chunks)

    excessive_chunks = sum(len(chunk["text"])>max_size 
                           for chunk in chunks)

    return {
        "total":len(chunks),
        "duplicates_id":duplicate_ids,
        "missing_source":missing_source,
        "empty_chunks":empty_chunks,
        "excessive_chunks":excessive_chunks
    }

def bm25_search(chunks, query, top_k=3):
    # Prepare chunk texts
    texts = [
        chunk["title"] + " "
        + chunk["section_title"] + " "
        + chunk["text"]
        for chunk in chunks
    ]

    # Split texts into words
    tokenized_texts = [
        re.findall(r"\b\w+\b", text.lower())
        for text in texts
    ]

    # Create BM25 model
    bm25 = BM25Okapi(tokenized_texts)

    # Prepare query
    query_tokens = re.findall(r"\b\w+\b", query.lower())

    # Rank chunks
    scores = bm25.get_scores(query_tokens)

    ranked_indices = sorted(
        range(len(chunks)),
        key=lambda i: scores[i],
        reverse=True
    )

    return [
        chunks[i]
        for i in ranked_indices[:top_k]
    ]

    
def evaluate_retrieval(cases, chunks):
    results = []

    for case in cases:
        retrieved = bm25_search(
            chunks,
            case["query"],
            top_k=3
        )

        success = any(
            chunk["source_id"] == case["expected_source"]
            and chunk["section_title"] == case["expected_section"]
            for chunk in retrieved
        )

        results.append({
            "case_id": case["case_id"],
            "success": success
        })

    return results



if __name__ == "__main__":
    documents = load_documents()
    cases = load_experiment_cases()
    print("Documents loaded:", len(documents))
    baseline_chunks = create_baseline_chunks(documents, chunk_size=500,overlap=50)
    save_chunks(baseline_chunks, "data/processed/chunks_baseline.jsonl")
    
    structure_chunks = create_structure_aware_chunks(documents, chunk_size=500,overlap=50)
    save_chunks(structure_chunks, "data/processed/chunks_structure.jsonl")
    save_chunks(structure_chunks,"data/processed/chunks_selected.jsonl")

    baseline_results = evaluate_retrieval(cases, baseline_chunks)
    structure_results = evaluate_retrieval(cases, structure_chunks)

    print("\nBaseline validation:")
    print(validate_chunks(baseline_chunks))
    print("\nStructure-aware validation:")
    print(validate_chunks(structure_chunks))

    print("\nRetrieval comparison:")
    for baseline, structure in zip(baseline_results, structure_results):
        print(
            baseline["case_id"],
            "| Baseline:", baseline["success"],
            "| Structure-aware:", structure["success"]
        )

    print(
        "Baseline successes:",
        sum(result["success"] for result in baseline_results),
        "/",
        len(cases)
    )

    print(
        "Structure-aware successes:",
        sum(result["success"] for result in structure_results),
        "/",
        len(cases)
    )

    print("\n=== BM25 RETRIEVAL DETAILS ===")

    for case in cases:
        print(f"\n{case['case_id']}: {case['query']}")

        baseline_top3 = bm25_search(
            baseline_chunks,
            case["query"],
            top_k=3
        )

        structure_top3 = bm25_search(
            structure_chunks,
            case["query"],
            top_k=3
        )

        print("Baseline:")
        for chunk in baseline_top3:
            print(" ", chunk["source_id"], "|", chunk["section_title"])

        print("Structure-aware:")
        for chunk in structure_top3:
            print(" ", chunk["source_id"], "|", chunk["section_title"])
