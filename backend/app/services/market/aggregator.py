from typing import Optional, Dict, Any, List
from app.services.market.yahoo_service import YahooFinanceService
from app.services.market.technical_service import TechnicalAnalysisService
from app.services.cache_service import cache_service
from app.schemas.market_data import MarketData, TechnicalIndicators
from loguru import logger

class MarketAggregator:
    @staticmethod
    async def get_comprehensive_data(ticker: str) -> Dict[str, Any]:
        # Try cache first
        cache_key = f"stock_data:{ticker}"
        cached_data = await cache_service.get(cache_key)
        if cached_data:
            logger.info(f"Returning cached data for {ticker}")
            return cached_data

        # Fetch basic info
        logger.info(f"Fetching fresh data for {ticker}")
        basic_info = YahooFinanceService.get_stock_info(ticker)
        if not basic_info:
            return {"error": "Could not fetch stock info"}

        # Fetch historical data for technical analysis
        historical_df = YahooFinanceService.get_historical_data(ticker, period="1y")
        
        # Calculate technical indicators
        indicators = TechnicalAnalysisService.calculate_indicators(historical_df)

        # Build response
        response = {
            "info": basic_info.dict(),
            "indicators": indicators.dict(),
            "last_updated": str(historical_df.index[-1]) if not historical_df.empty else None
        }

        # Cache for 1 hour
        await cache_service.set(cache_key, response, expire=3600)
        
        return response

    @staticmethod
    def get_historical_points(ticker: str, period: str = "1y") -> List[Dict[str, Any]]:
        df = YahooFinanceService.get_historical_data(ticker, period=period)
        if df.empty:
            return []
        
        df.reset_index(inplace=True)
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        return df.to_dict('records')
