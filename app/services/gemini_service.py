from fastapi import APIRouter
import requests
from ..config import GEMINI_KEY

router = APIRouter(tags=["Gemini"])

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

async def ask_gemini(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_KEY}", headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return "⚠️ No valid response from Gemini"

@router.post("/gemini")
async def gemini_query(payload: dict):
    prompt = payload.get("prompt", "")
    return {"response": await ask_gemini(prompt)}

@router.post("/chat")
async def chat_query(payload: dict):
    message = payload.get("message", "")
    return {"response": await ask_gemini(message)}
