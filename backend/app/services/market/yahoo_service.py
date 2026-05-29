import yfinance as yf
import pandas as pd
from typing import Optional, Dict, Any
from app.schemas.market_data import MarketData, HistoricalPoint

class YahooFinanceService:
    @staticmethod
    def get_stock_info(ticker: str) -> Optional[MarketData]:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return MarketData(
                ticker=ticker,
                company_name=info.get("longName"),
                exchange=info.get("exchange"),
                current_price=info.get("currentPrice") or info.get("regularMarketPrice") or 0.0,
                market_cap=info.get("marketCap"),
                volume=info.get("volume"),
                open=info.get("open"),
                high=info.get("dayHigh"),
                low=info.get("dayLow"),
                close=info.get("previousClose"),
                pe_ratio=info.get("forwardPE"),
                eps=info.get("trailingEps"),
                revenue_growth=info.get("revenueGrowth"),
                debt_to_equity=info.get("debtToEquity"),
                roe=info.get("returnOnEquity"),
                sector=info.get("sector"),
                industry=info.get("industry")
            )
        except Exception as e:
            print(f"Error fetching Yahoo Finance data for {ticker}: {e}")
            return None

    @staticmethod
    def get_historical_data(ticker: str, period: str = "1y") -> pd.DataFrame:
        """
        Periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        """
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period)
            return df
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            return pd.DataFrame()
