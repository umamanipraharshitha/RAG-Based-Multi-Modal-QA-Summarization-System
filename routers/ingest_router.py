# app/routers/ingest_router.py
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from ..services.ingest_service import ingest_plain_text, ingest_file

router = APIRouter(prefix="/ingest", tags=["Ingest"])

# ---- Existing JSON text ingest (unchanged behavior) ----
class IngestPayload(BaseModel):
    doc_id: str
    text: str

@router.post("/", summary="Ingest plain text (JSON)")
def ingest_text(payload: IngestPayload):
    return ingest_plain_text(payload.doc_id, payload.text)

# ---- NEW: Multi-file ingest via multipart/form-data ----
@router.post("/file", summary="Ingest one or more files (PDF, DOCX, CSV, images)")
async def ingest_files(
    files: List[UploadFile] = File(..., description="Upload one or more files"),
    doc_id_prefix: Optional[str] = Form(default="doc", description="Prefix to group these files"),
):
    results = []
    for f in files:
        data = await f.read()
        results.append(ingest_file(doc_id_prefix, f.filename, data, f.content_type))
    return {"message": "Files processed", "results": results}
