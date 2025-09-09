# app/services/embeddings_service.py
from typing import List
import threading
import asyncio
from sentence_transformers import SentenceTransformer

_model = None
_model_lock = threading.Lock()
_model_ready = threading.Event()

def _load_model():
    global _model
    with _model_lock:
        if _model is None:
            print("⏳ Downloading/loading SentenceTransformer model...")
            _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            print("✅ Model loaded!")
            _model_ready.set()

threading.Thread(target=_load_model, daemon=True).start()

async def embed_texts(texts: List[str]) -> List[List[float]]:
    if not _model_ready.is_set():
        print("⏳ Waiting for model to be ready...")
        await asyncio.to_thread(_model_ready.wait)
    return await asyncio.to_thread(lambda: _model.encode(texts, show_progress_bar=False).tolist())

async def embed_text(text: str) -> List[float]:
    result = await embed_texts([text])
    return result[0]
