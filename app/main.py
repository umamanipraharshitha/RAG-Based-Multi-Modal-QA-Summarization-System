from fastapi import FastAPI
from app.services.gemini_service import router as gemini_router
from app.services.ingest_service import router as ingest_router
from app.services.query_service import router as query_router
from app.services.qa_service import router as qa_router
from app.services.embeddings_router import router as embeddings_router
app = FastAPI(
    title="Kai Hub",
    description="Gemini + GPT-4o RAG API",
    version="1.0.0"
)

# Include routers
app.include_router(gemini_router, prefix="")  # <-- important
app.include_router(ingest_router, prefix="")
app.include_router(query_router, prefix="")
app.include_router(qa_router, prefix="")

@app.get("/")
async def root():
    return {"message": "Welcome to Kai Hub API"}
