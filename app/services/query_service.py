from fastapi import APIRouter
from ..models import QueryPayload
from .ingest_service import collection
from .gemini_service import ask_gemini

router = APIRouter()

def retrieve_documents(query: str, top_k: int = 3):
    results = collection.query(query_texts=[query], n_results=top_k)
    return results.get("documents", [[]])[0]

@router.post("/")
async def answer_question(payload: QueryPayload):
    docs = retrieve_documents(payload.query, payload.top_k)
    if not docs:
        return {"answer": "No relevant documents found."}
    context = "\n---\n".join(docs)
    prompt = f"Use the following context to answer the question:\n\n{context}\n\nQ: {payload.query}\nA:"
    answer = await ask_gemini(prompt)
    return {"answer": answer}
