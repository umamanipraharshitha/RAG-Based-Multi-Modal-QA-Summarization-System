import chromadb
from chromadb.utils import embedding_functions
from ..config import OPENAI_KEY, CHROMA_DB_PATH

# Persistent Chroma client
client_chroma = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Embedding function (OpenAI)
ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_KEY,
    model_name="text-embedding-3-large"
)

# Create or get collection
collection = client_chroma.get_or_create_collection(
    name="kai_docs",
    embedding_function=ef
)

def add_document(doc_id: str, text: str, meta: dict):
    collection.add(ids=[doc_id], documents=[text], metadatas=[meta])
