import pytest
from unittest.mock import patch, AsyncMock
from app.services.gemini_service import ask_gemini


@pytest.mark.asyncio
async def test_ask_gemini_returns_string():
    """Test ask_gemini returns a string for a valid API response."""
    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value={
        "candidates": [{"content": {"parts": [{"text": "FastAPI is a Python web framework."}]}}]
    })
    mock_response.raise_for_status = lambda: None

    async def mock_post(*args, **kwargs):
        return mock_response

    mock_client = AsyncMock()
    mock_client.post = mock_post

    with patch("httpx.AsyncClient", return_value=mock_client):
        response = await ask_gemini("Summarize: FastAPI")

    assert isinstance(response, str)
    assert "FastAPI" in response

