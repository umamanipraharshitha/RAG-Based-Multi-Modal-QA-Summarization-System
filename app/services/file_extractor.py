# app/services/file_extractor.py
from typing import List, Tuple, Optional
import io
import csv
from PIL import Image
import pandas as pd

# --- PDF ---
import fitz  # PyMuPDF

# --- DOCX ---
from docx import Document

# --- OCR ---
import pytesseract

# If on Windows and Tesseract isn't in PATH, set it here:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(data: bytes) -> str:
    text_parts: List[str] = []
    with fitz.open(stream=data, filetype="pdf") as doc:
        for page in doc:
            text_parts.append(page.get_text("text"))
    return "\n".join(text_parts).strip()

def extract_text_from_docx(data: bytes) -> str:
    file_obj = io.BytesIO(data)
    doc = Document(file_obj)
    return "\n".join([p.text for p in doc.paragraphs]).strip()

def extract_text_from_csv(data: bytes) -> str:
    # Prefer pandas for robustness; falls back to csv if needed
    try:
        df = pd.read_csv(io.BytesIO(data), encoding_errors="ignore")
        # Concatenate all text-like columns row-wise
        text_cols = [c for c in df.columns if df[c].dtype == "object"]
        if not text_cols:
            # If no object cols, stringify everything
            text_cols = list(df.columns)
        return "\n".join(df[text_cols].astype(str).agg(" | ".join, axis=1).tolist()).strip()
    except Exception:
        text_lines: List[str] = []
        file_obj = io.StringIO(data.decode(errors="ignore"))
        reader = csv.reader(file_obj)
        for row in reader:
            text_lines.append(" | ".join(row))
        return "\n".join(text_lines).strip()

def extract_text_from_image(data: bytes) -> str:
    image = Image.open(io.BytesIO(data)).convert("RGB")
    text = pytesseract.image_to_string(image)
    return text.strip()

def detect_and_extract(filename: str, data: bytes, content_type: Optional[str]) -> Tuple[str, str]:
    """
    Returns (extracted_text, source_kind)
    source_kind in {"pdf","docx","csv","image","text"}
    """
    name = filename.lower()

    # Favor MIME if present
    if content_type:
        ct = content_type.lower()
        if "pdf" in ct:
            return extract_text_from_pdf(data), "pdf"
        if "word" in ct or "officedocument.wordprocessingml.document" in ct:
            return extract_text_from_docx(data), "docx"
        if "csv" in ct:
            return extract_text_from_csv(data), "csv"
        if "image" in ct:
            return extract_text_from_image(data), "image"
        if "text" in ct or "plain" in ct:
            return data.decode(errors="ignore").strip(), "text"

    # Fallback by extension
    if name.endswith(".pdf"):
        return extract_text_from_pdf(data), "pdf"
    if name.endswith(".docx"):
        return extract_text_from_docx(data), "docx"
    if name.endswith(".csv"):
        return extract_text_from_csv(data), "csv"
    if any(name.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"]):
        return extract_text_from_image(data), "image"

    # Plain text fallback
    return data.decode(errors="ignore").strip(), "text"
