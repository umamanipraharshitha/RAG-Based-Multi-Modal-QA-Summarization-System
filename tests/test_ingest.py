import pytest
from app.services.ingest_service import collection

def test_add_document():
    doc_id = "test_doc_1"
    text = "FastAPI is a Python web framework."
    meta = {"source": "wiki"}  # optional

    # Use collection.add directly
    collection.add(
        documents=[text],
        ids=[doc_id],
        metadatas=[meta]  # only if your collection supports metadatas
    )

    # Query the collection
    results = collection.query(query_texts=[text], n_results=1)
    retrieved_docs = results.get("documents", [[]])[0]

    assert text in retrieved_docs, "Document not added correctly"
