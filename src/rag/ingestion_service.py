import csv
from pathlib import Path
from collections import Counter
from docx import Document
import json
import hashlib
from datetime import datetime, timezone


POLICIES_DIR = Path("docs/policies")
MANIFEST_PATH = POLICIES_DIR / "05_Manifests_and_Guides" / "knowledge_base_manifest.csv"

REQUIRED_FIELDS = {
    "source_id",
    "title",
    "document_type",
    "version",
    "effective_date",
    "access_label",
    "status",
    "relative_path",
}

def calculate_checksum(file_path):
    with open(file_path, "rb") as file:
        return hashlib.sha256(file.read()).hexdigest()

def missing_required_fields(document):
    return [
        field
        for field in REQUIRED_FIELDS
        if not document.get(field, "").strip()
    ]

def load_manifest():
    with open(MANIFEST_PATH, "r", encoding = "utf-8-sig") as file:
        reader = csv.DictReader(file)
        return list(reader)


def find_source_files():
    return list(POLICIES_DIR.rglob("*.docx")) ## recherche les fichiers
                                              ## .docx dans le dossier POLICIES_DIR et ses sous-dossiers


def validate_sources(manifest, source_files):
    accepted = []
    rejected = []
    warnings = []

    manifest_paths = set()

    id_counts = Counter(doc["source_id"] for doc in manifest)

    path_counts = Counter(
        str((POLICIES_DIR / doc["relative_path"]).resolve())
        for doc in manifest
    )

    for document in manifest:
        # check if mandatory fields are present and not empty
        missing = missing_required_fields(document)
        if missing:
            rejected.append({"source_id": document.get("source_id", "Unknown"),"reason": f"Missing required fields: {', '.join(missing)}"})
        source_id = document["source_id"]
        relative_path = document["relative_path"]

        file_path = POLICIES_DIR / relative_path
        resolved_path = file_path.resolve()

        is_allowed = resolved_path.is_relative_to(POLICIES_DIR.resolve())
        if not is_allowed:
            rejected.append({"source_id": source_id, "reason": "Path is outside the allowed directory"})
            continue

        manifest_paths.add(resolved_path)

        #for duplicate source id or file path
        if id_counts[source_id] > 1 or path_counts[str(resolved_path)] > 1:
            rejected.append({
                "source_id": source_id,
                "reason": "Duplicate source_id or path"
            })
            continue

        # for missing file
        if not file_path.exists():
            rejected.append({"source_id": source_id, "reason": "Source file not found"})
            continue

        # for unapproved document
        if document["status"]!="Approved":
            rejected.append({"source_id": source_id, "reason": f"Document status is {document['status']}, not Approved"})
            continue

        accepted.append({"source_id": source_id, "path": resolved_path})

    # for files not in manifest
    for file_path in source_files:
        if file_path.resolve() not in manifest_paths:
            rejected.append({"path": str(file_path), "reason": "File not listed in manifest"})

    return {"accepted": accepted,"rejected": rejected,"warnings": warnings}


def extract_paragraphs(file_path):
    doc = Document(file_path)
    paragraphs = []

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip() # supprime les espaces inutiles au début et à la fin du texte
        if text:
            paragraphs.append({"text": text, "style": paragraph.style.name})

    return paragraphs


def extract_sections(paragraphs, source_id):
    sections = []
    section_title = "Introduction"
    content = []

    for para in paragraphs:
        text = para["text"]
        style = para["style"]

        if style.startswith("Heading"):
            if content:
                sections.append({
                    "source_id": source_id,
                    "section_title": section_title,
                    "content": content
                })
            section_title = text
            content=[]
        elif style=="Normal":
            content.append(text)
    if content:
        sections.append({
            "source_id": source_id,
            "section_title": section_title,
            "content": content
        })
    return sections



def save_documents(sections):
    output_path = Path("data/processed/documents.jsonl")
    output_path.parent.mkdir(parents=True, exist_ok=True) # cree le dossier de sortie s'il n'existe pas

    with open(output_path, "w", encoding="utf-8") as file:
        for section in sections:
            file.write(json.dumps(section, ensure_ascii=False) + "\n")



def save_run_log(result):
    log={
        "run_time": datetime.now(timezone.utc).isoformat(),
        "accepted": len(result["accepted"]),
        "rejected": len(result["rejected"]),
        "warnings": len(result["warnings"]),
        "rejected_files": result["rejected"]
    }

    with open("ingestion_run_log.json","w", encoding="utf-8") as file:
        json.dump(log, file, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    manifest = load_manifest()
    source_files = find_source_files()

    result = validate_sources(manifest, source_files)

    print("Accepted Sources:", result["accepted"])
    print("\n ------------------------------------------------------------\n")
    print("Rejected Sources:", result["rejected"])
    print("\n ------------------------------------------------------------\n")
    print("Warnings:", result["warnings"])


    first_file = result["accepted"][0]["path"]
    paragraphs = extract_paragraphs(first_file)

    print(f"Source : {result['accepted'][0]['source_id']}")

    for para in paragraphs:
        print(para)

    sections = extract_sections(paragraphs, result["accepted"][0]["source_id"])

    print(f"Extracted sections: {len(sections)}")

    for section in sections[:3]:
        print("\nSource:", section["source_id"])
        print("Section:", section["section_title"])
        print("Content:", section["content"][:200])

    all_sections = []

    for source in result["accepted"]:
        paragraphs = extract_paragraphs(source["path"])
        sections = extract_sections(paragraphs, source["source_id"])

        metadata = next(
            doc for doc in manifest
            if doc["source_id"] == source["source_id"]
        )
        checksum = calculate_checksum(source["path"])

        for sequence, section in enumerate(sections, start=1):
            section["title"] = metadata["title"]
            section["document_type"] = metadata["document_type"]
            section["version"] = metadata["version"]
            section["effective_date"] = metadata["effective_date"]
            section["status"] = metadata["status"]
            section["access_label"] = metadata["access_label"]
            section["relative_path"] = metadata["relative_path"]
            section["sequence"] = sequence
            section["chunk_id"] = f"{source['source_id']}#section#{sequence:04d}"
            section["checksum"] = checksum

        all_sections.extend(sections)
    print("Sections before saving:", len(all_sections))
    save_documents(all_sections)
    save_run_log(result)

    print(f"Documents processed: {len(result['accepted'])}")
    print(f"Sections exported: {len(all_sections)}")
    print("Output: data/processed/documents.jsonl")