from typing import Any
from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_model=dict)
def get_portfolio() -> Any:
    """
    Get user's current portfolio holdings and performance metrics.
    """
    # Mock return for structure
    return {
        "holdings": [
            {"ticker": "AAPL", "shares": 10, "avg_price": 150.0, "current_price": 175.0, "gain_loss": 250.0}
        ],
        "total_value": 1750.0,
        "total_gain": 250.0
    }

@router.post("/add", response_model=dict)
def add_to_portfolio(ticker: str, shares: float, price: float) -> Any:
    return {"message": f"Added {shares} shares of {ticker} at {price}."}

@router.delete("/remove", response_model=dict)
def remove_from_portfolio(ticker: str) -> Any:
    return {"message": f"Removed {ticker} from portfolio."}
