from pydantic import BaseModel

class IngestPayload(BaseModel):
    id: str
    text: str
    meta: dict = {}

class QueryPayload(BaseModel):
    query: str
    top_k: int = 3
