from typing import Any
from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_model=dict)
def get_watchlist() -> Any:
    """
    Get user's current watchlist.
    """
    return {
        "items": [
            {"ticker": "MSFT", "current_price": 400.0},
            {"ticker": "TSLA", "current_price": 180.0}
        ]
    }

@router.post("/add", response_model=dict)
def add_to_watchlist(ticker: str) -> Any:
    return {"message": f"Added {ticker} to watchlist."}

@router.delete("/remove", response_model=dict)
def remove_from_watchlist(ticker: str) -> Any:
    return {"message": f"Removed {ticker} from watchlist."}
