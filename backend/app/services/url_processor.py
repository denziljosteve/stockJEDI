import re
from typing import Optional, Tuple
from urllib.parse import urlparse

class URLProcessor:
    SOURCES = {
        "finance.yahoo.com": "Yahoo Finance",
        "www.screener.in": "Screener.in",
        "www.tradingview.com": "TradingView",
        "www.nseindia.com": "NSE",
        "www.bseindia.com": "BSE",
        "www.moneycontrol.com": "Moneycontrol",
        "www.marketwatch.com": "MarketWatch",
        "seekingalpha.com": "Seeking Alpha"
    }

    @classmethod
    def process_url(cls, url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract ticker and source from a URL.
        Returns (ticker, source)
        """
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        source = cls.SOURCES.get(domain, "Unknown")
        ticker = None

        if "yahoo" in domain:
            # https://finance.yahoo.com/quote/AAPL
            match = re.search(r"/quote/([A-Z0-9.-]+)", url)
            if match:
                ticker = match.group(1)
        elif "screener.in" in domain:
            # https://www.screener.in/company/RELIANCE/
            match = re.search(r"/company/([A-Z0-9-]+)", url)
            if match:
                ticker = match.group(1)
        elif "tradingview.com" in domain:
            # https://www.tradingview.com/symbols/NASDAQ-AAPL/
            match = re.search(r"/symbols/([A-Z0-9:-]+)", url)
            if match:
                ticker = match.group(1).split("-")[-1]
        elif "marketwatch.com" in domain:
            # https://www.marketwatch.com/investing/stock/aapl
            match = re.search(r"/investing/stock/([a-z0-9.-]+)", url.lower())
            if match:
                ticker = match.group(1).upper()
        elif "moneycontrol.com" in domain:
            # https://www.moneycontrol.com/india/stockpricequote/refineries/relianceindustries/RI
            parts = url.split("/")
            if len(parts) > 0:
                ticker = parts[-1].upper()
        elif "nseindia.com" in domain or "bseindia.com" in domain:
            # https://www.nseindia.com/get-quotes/equity?symbol=RELIANCE
            match = re.search(r"symbol=([A-Z0-9&]+)", url)
            if match:
                ticker = match.group(1)
        
        # Add more logic for other sources as needed
        
        return ticker, source

    @classmethod
    def validate_ticker(cls, ticker: str) -> bool:
        """
        Basic validation for a ticker symbol.
        """
        if not ticker:
            return False
        # Tickers are usually alphanumeric, 1-10 chars
        return bool(re.match(r"^[A-Z0-9.-]{1,10}$", ticker))
