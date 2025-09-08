import pytest
from unittest.mock import patch, AsyncMock
from app.services.gemini_service import ask_gemini


@pytest.mark.asyncio
async def test_ask_gemini_returns_string():
    """Test ask_gemini returns a string for a valid API response."""
    with patch("app.services.gemini_service.httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        # Mock success response
        mock_post.return_value.json = lambda: {
            "candidates": [{"content": {"parts": [{"text": "FastAPI is a Python web framework."}]}}]
        }
        mock_post.return_value.raise_for_status = lambda: None

        response = await ask_gemini("Summarize: FastAPI")
        assert isinstance(response, str)
        assert "FastAPI" in response


@pytest.mark.asyncio
async def test_ask_gemini_handles_error():
    """Test ask_gemini handles invalid/empty API responses gracefully."""
    with patch("app.services.gemini_service.httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        # Mock invalid response
        mock_post.return_value.json = lambda: {}
        mock_post.return_value.raise_for_status = lambda: None

        response = await ask_gemini("Invalid response test")
        assert response == "⚠️ No valid response from Gemini"
