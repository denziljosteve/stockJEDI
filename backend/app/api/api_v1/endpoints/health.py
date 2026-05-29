from typing import Any
from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_model=dict)
def health_check() -> Any:
    """
    Check if the API is healthy.
    """
    return {"status": "ok"}
