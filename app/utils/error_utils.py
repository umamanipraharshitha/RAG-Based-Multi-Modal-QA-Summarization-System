from fastapi import HTTPException
from typing import Any

def http_error(msg: str | dict[str, Any], code: int = 400) -> None:
    """
    Raise a FastAPI HTTPException with custom message and status code.

    Args:
        msg (str | dict): Error message or structured error details.
        code (int): HTTP status code (default 400).
    """
    raise HTTPException(status_code=code, detail=msg)
