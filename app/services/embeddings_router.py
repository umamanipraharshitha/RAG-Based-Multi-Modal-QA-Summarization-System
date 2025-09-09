# app/services/embeddings_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from .embeddings_service import embed_text, embed_texts

router = APIRouter(prefix="/embeddings", tags=["Embeddings"])

class TextRequest(BaseModel):
    text: str

class TextsRequest(BaseModel):
    texts: list[str]

@router.post("/text")
async def get_embedding(req: TextRequest):
    return {"embedding": await embed_text(req.text)}

@router.post("/texts")
async def get_embeddings(req: TextsRequest):
    return {"embeddings": await embed_texts(req.texts)}
