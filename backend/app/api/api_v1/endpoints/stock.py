from typing import Any, List
from fastapi import APIRouter, HTTPException, status

from app.schemas.stock import Stock, StockExtractRequest, StockExtractResponse
from app.services.url_processor import URLProcessor

from app.services.market.aggregator import MarketAggregator

router = APIRouter()

@router.get("/search", response_model=List[Stock])
def search_stock(q: str) -> Any:
    """
    Search for a stock by name or ticker.
    """
    # Placeholder
    return []

@router.post("/extract", response_model=StockExtractResponse)
def extract_stock_from_url(request: StockExtractRequest) -> Any:
    """
    Extract ticker from a stock URL.
    """
    ticker, source = URLProcessor.process_url(str(request.url))
    is_valid = False
    if ticker:
        is_valid = URLProcessor.validate_ticker(ticker)

    return StockExtractResponse(
        ticker=ticker,
        source=source,
        is_valid=is_valid
    )

@router.post("/analyze", response_model=dict)
async def analyze_stock(ticker: str) -> Any:
    """
    Start analysis for a specific stock.
    """
    data = await MarketAggregator.get_comprehensive_data(ticker)
    if "error" in data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=data["error"]
        )
    return data

@router.get("/{ticker}/historical", response_model=List[dict])
def get_historical_data(ticker: str, period: str = "1y") -> Any:
    """
    Get historical price data for a stock.
    """
    data = MarketAggregator.get_historical_points(ticker, period=period)
    return data

