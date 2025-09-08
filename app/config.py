import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# Optional: store Chroma server URL or host/port here
CHROMA_SERVER_HOST = "localhost"
CHROMA_SERVER_PORT = 8000

# API Keys
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# ChromaDB (running as a server)
CHROMA_SERVER_URL = os.getenv("CHROMA_SERVER_URL", "http://localhost:8000")

# Gemini model config
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
