from typing import Any, List
from fastapi import APIRouter, HTTPException, status
import yfinance as yf

from app.schemas.stock import Stock, StockExtractRequest, StockExtractResponse
from app.services.url_processor import URLProcessor
from app.services.market.aggregator import MarketAggregator

router = APIRouter()


@router.get("/search", response_model=List[Stock])
def search_stock(q: str) -> Any:
    if not q or not q.strip():
        return []

    query = q.strip()

    try:
        results = yf.Search(query, max_results=10, news_count=0)
        tickers = []
        for item in results.quotes:
            symbol = item.get("symbol", "")
            name = item.get("shortName") or item.get("longName") or ""
            exchange = item.get("exchange") or ""
            if symbol:
                tickers.append(Stock(ticker=symbol, name=name, source=exchange))
        return tickers
    except Exception:
        pass

    try:
        stock = yf.Ticker(query)
        info = stock.info
        symbol = info.get("symbol") or info.get("ticker")
        name = info.get("longName") or info.get("shortName") or ""
        exchange = info.get("exchange") or ""
        if symbol:
            return [Stock(ticker=symbol, name=name, source=exchange)]
    except Exception:
        pass

    return []


@router.post("/extract", response_model=StockExtractResponse)
def extract_stock_from_url(request: StockExtractRequest) -> Any:
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
    data = await MarketAggregator.get_comprehensive_data(ticker)
    if "error" in data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=data["error"]
        )
    return data


@router.get("/{ticker}/historical", response_model=List[dict])
def get_historical_data(ticker: str, period: str = "1y") -> Any:
    data = MarketAggregator.get_historical_points(ticker, period=period)
    return data
