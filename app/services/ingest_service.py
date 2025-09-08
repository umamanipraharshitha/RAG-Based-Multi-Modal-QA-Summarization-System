# app/services/ingest_service.py
import os
import io
import fitz  # PyMuPDF
import docx
import pytesseract
import pandas as pd
from PIL import Image
from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
import chromadb

router = APIRouter(prefix="/ingest", tags=["Ingest"])

# ✅ Persistent ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# ✅ Create/get collection
collection = chroma_client.get_or_create_collection("kai_collection")


# --------------------------
# Text ingestion model
# --------------------------
class Document(BaseModel):
    doc_id: str
    text: str


@router.post("/")
async def ingest_document(doc: Document):
    """
    Ingest plain text into the vector DB.
    """
    try:
        collection.add(documents=[doc.text], ids=[doc.doc_id])
        return {"message": f"Document {doc.doc_id} ingested successfully!"}
    except Exception as e:
        return {"error": str(e)}


# --------------------------
# Multi-modal ingestion
# --------------------------
@router.post("/file")
async def ingest_file(doc_id: str = Form(...), file: UploadFile = File(...)):
    """
    Ingest PDFs, Word docs, CSVs, or images.
    Extract text, then push into ChromaDB.
    """
    try:
        filename = file.filename.lower()
        contents = await file.read()
        text = ""

        if filename.endswith(".pdf"):
            # Extract text from PDF using PyMuPDF
            pdf = fitz.open(stream=contents, filetype="pdf")
            text = "\n".join(page.get_text() for page in pdf)

        elif filename.endswith(".docx"):
            # Extract text from Word doc
            doc = docx.Document(io.BytesIO(contents))
            text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())

        elif filename.endswith(".csv"):
            # Convert CSV to text
            df = pd.read_csv(io.BytesIO(contents))
            text = df.to_string(index=False)

        elif filename.endswith((".png", ".jpg", ".jpeg")):
            # OCR with pytesseract
            image = Image.open(io.BytesIO(contents))
            text = pytesseract.image_to_string(image)

        else:
            return {"error": "Unsupported file format."}

        if not text.strip():
            return {"error": "No text extracted from file."}

        # ✅ Real-time embedding update
        collection.add(documents=[text], ids=[doc_id])

        return {"message": f"File {file.filename} ingested successfully!", "chars": len(text)}

    except Exception as e:
        return {"error": str(e)}
