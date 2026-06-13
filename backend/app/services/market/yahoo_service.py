import yfinance as yf
import pandas as pd
from typing import Optional, Dict, Any
from loguru import logger
from app.schemas.market_data import MarketData, HistoricalPoint

class YahooFinanceService:
    REQUEST_TIMEOUT = 30

    @staticmethod
    def get_stock_info(ticker: str) -> Optional[MarketData]:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            if not info or info.get('trailingPegRatio') is None:
                logger.warning(f"No data returned for ticker {ticker}")

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
        except ConnectionError as e:
            logger.error(f"Network error fetching Yahoo Finance data for {ticker}: {e}")
            return None
        except TimeoutError as e:
            logger.error(f"Timeout fetching Yahoo Finance data for {ticker}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching Yahoo Finance data for {ticker}: {e}")
            return None

    @staticmethod
    def get_historical_data(ticker: str, period: str = "1y") -> pd.DataFrame:
        """
        Periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        """
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period)
            if df.empty:
                logger.warning(f"No historical data returned for {ticker}")
            return df
        except ConnectionError as e:
            logger.error(f"Network error fetching historical data for {ticker}: {e}")
            return pd.DataFrame()
        except TimeoutError as e:
            logger.error(f"Timeout fetching historical data for {ticker}: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error fetching historical data for {ticker}: {e}")
            return pd.DataFrame()
