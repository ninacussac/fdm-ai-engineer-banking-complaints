from src.rag.ingestion_service import load_manifest,find_source_files, validate_sources


def test_valid_manifest():
    manifest = load_manifest()
    source_files = find_source_files()

    result = validate_sources(manifest, source_files)

    assert len(result["accepted"]) == 12
    assert all(
        source["source_id"] != "KB-001-OLD"
        for source in result["accepted"]
    )



def test_unlisted_file():
    manifest = load_manifest()
    source_files = find_source_files()

    # Simulate an additional unlisted file
    unknown_file = source_files[0].parent / "unknown_policy.docx"
    source_files.append(unknown_file)

    result = validate_sources(manifest, source_files)

    assert any(
        item.get("reason") == "File not listed in manifest"
        and item.get("path") == str(unknown_file)
        for item in result["rejected"]
    )


def test_duplicate_source_id():
    manifest = load_manifest()
    source_files = find_source_files()

    # Duplicate the first manifest entry
    test_manifest = [doc.copy() for doc in manifest]
    test_manifest.append(manifest[0].copy())

    result = validate_sources(test_manifest, source_files)

    duplicates = [
        item for item in result["rejected"]
        if item.get("source_id") == "KB-001"
        and item.get("reason") == "Duplicate source_id or path"
    ]

    assert len(duplicates) == 2


def test_missing_effective_date():
    manifest = load_manifest()
    source_files = find_source_files()

    # Remove the effective date from KB-001
    test_manifest = [doc.copy() for doc in manifest]
    test_manifest[0]["effective_date"] = ""

    result = validate_sources(test_manifest, source_files)

    assert any(
        item.get("source_id") == "KB-001"
        and "effective_date" in item.get("reason", "")
        for item in result["rejected"]
    )