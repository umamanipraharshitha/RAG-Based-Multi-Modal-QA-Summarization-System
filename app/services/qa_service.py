# app/services/qa_service.py
from fastapi import APIRouter
from ..models import QueryPayload
from .ingest_service import collection
from .gemini_service import ask_gemini

router = APIRouter(prefix="/qa", tags=["QA"])


# --------------------------
# Document retrieval
# --------------------------
def retrieve_documents(query: str, top_k: int = 5):
    """
    Retrieve documents using hybrid search:
    - Semantic search via ChromaDB
    - Keyword search
    """
    # Step 1: Semantic search
    sem_results = collection.query(query_texts=[query], n_results=top_k)
    sem_docs = sem_results.get("documents", [[]])[0]

    # Step 2: Keyword search
    all_docs = collection.get(include=["documents"])["documents"]
    keyword_docs = [doc for doc in all_docs if query.lower() in doc.lower()]

    # Step 3: Merge & deduplicate
    final_docs = list(dict.fromkeys(sem_docs + keyword_docs))
    return final_docs[:top_k]


# --------------------------
# Optional reranking with Gemini
# --------------------------
async def rerank_documents(query: str, docs: list):
    if not docs:
        return []

    prompt = f"Rank the following documents by relevance to the query:\nQuery: {query}\nDocuments:\n"
    for i, doc in enumerate(docs):
        prompt += f"{i+1}. {doc}\n"
    prompt += "Return the indices of the most relevant documents first, separated by commas."

    try:
        ranking = await ask_gemini(prompt)  # e.g., returns "2,1,3"
        indices = [int(x.strip()) - 1 for x in ranking.split(",") if x.strip().isdigit()]
        return [docs[i] for i in indices if i < len(docs)]
    except Exception:
        # fallback to original order if Gemini fails
        return docs


# --------------------------
# QA endpoint
# --------------------------
@router.post("/")
async def answer_question(payload: QueryPayload):
    # Step 1: Retrieve documents
    docs = retrieve_documents(payload.query, payload.top_k)

    if not docs:
        return {"answer": "No relevant documents found."}

    # Step 2: Rerank documents (optional, Gemini-powered)
    docs = await rerank_documents(payload.query, docs)

    # Step 3: Prepare context and ask Gemini
    context = "\n---\n".join(docs)
    prompt = f"Use the following context to answer the question:\n\n{context}\n\nQ: {payload.query}\nA:"

    answer = await ask_gemini(prompt)

    return {"answer": answer}
