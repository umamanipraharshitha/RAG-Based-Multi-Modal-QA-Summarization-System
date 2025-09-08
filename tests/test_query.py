import pytest
from app.services.query_service import retrieve_documents

@pytest.mark.asyncio
async def test_retrieve_documents():
    # Make sure collection has at least one document ingested
    query = "FastAPI web framework"
    docs = retrieve_documents(query, top_k=1)

    assert isinstance(docs, list), "Should return a list of documents"
    assert len(docs) <= 1, "Retrieved more than requested"
    if docs:
        assert "FastAPI" in docs[0], "Retrieved document does not match query"
