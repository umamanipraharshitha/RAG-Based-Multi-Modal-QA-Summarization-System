# RAG-Based Multi-Modal QA Summarization System(Ongoing)

A **Retrieval-Augmented Generation (RAG)** system that enables querying over multiple document types (PDF, DOCX, CSV, Images, plain text) and generates answers using embeddings and LLM reranking via Gemini.

---

## Features with individual modules 

- **Multi-modal ingestion**: Supports PDFs, Word documents, CSVs, and images (OCR).
- **Text extraction**: Uses `PyMuPDF`, `python-docx`, `pandas`, and `pytesseract`.
- **Semantic search**: Embeddings with `sentence-transformers` stored in **ChromaDB**.
- **Keyword fallback**: Finds exact matches if semantic search fails.
- **Optional LLM reranking**: Uses **Gemini API** to rank retrieved documents by relevance.
- **QA pipeline**: Returns final answer along with source documents.
- **FastAPI backend**: Easy-to-use REST API for ingestion and question answering.

---
Current flowchart TD
    A[User Query / File Upload] --> B{Is it a file or query?}

    B -->|File| C[File Ingestion Endpoint]
    C --> D[Text Extraction using file_extractor.py]
    D --> E[Chunking Text with ingest_service.chunk_text]
    E --> F[Store Chunks in ChromaDB]

    B -->|Query| G[Query Endpoint]
    G --> H[Retrieve documents from ChromaDB]
    H --> I[Optional Gemini Rerank (ask_gemini)]
    I --> J[Prepare Context for LLM]

    J --> K[Generate Answer using Gemini API]
    K --> L[Return Answer + Source Documents to User]


## Tech Stack

- **Backend**: Python, FastAPI
- **Embedding**: `sentence-transformers` (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB (persistent)
- **File Parsing**: PyMuPDF, python-docx, pandas, Pillow, pytesseract
- **LLM API**: Google Gemini
- **Deployment**: Local / Cloud-ready

---

## Installation

```bash
git clone https://github.com/umamanipraharshitha/RAG-Based-Multi-Modal-QA-Summarization-System.git
cd RAG-Based-Multi-Modal-QA-Summarization-System
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
Usage
1. Start the FastAPI server
uvicorn app.main:app --reload

2. Ingest files
POST /qa_pipeline/ingest_file
Form Data:
- doc_id: unique document ID
- file: upload PDF/DOCX/CSV/Image

3. Ask a question
POST /qa_pipeline/answer
JSON:
{
  "query": "Your question here",
  "top_k": 5
}
