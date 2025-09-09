from fastapi import APIRouter, UploadFile, File
from .file_extractor import detect_and_extract

router = APIRouter(prefix="/files", tags=["File Extractor"])

@router.post("/extract")
async def extract_file(file: UploadFile = File(...)):
    data = await file.read()
    text, kind = detect_and_extract(file.filename, data, file.content_type)
    return {
        "filename": file.filename,
        "kind": kind,
        "text": text[:500]  # limit preview in response
    }
