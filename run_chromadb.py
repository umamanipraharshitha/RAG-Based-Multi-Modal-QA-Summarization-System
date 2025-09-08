from chromadb.server import fastapi
import uvicorn

app = fastapi.app  # use 'app' directly from chromadb.server.fastapi

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
