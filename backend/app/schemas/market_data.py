from typing import Optional, List
from pydantic import BaseModel

class MarketData(BaseModel):
    ticker: str
    company_name: Optional[str] = None
    exchange: Optional[str] = None
    current_price: float
    market_cap: Optional[float] = None
    volume: Optional[int] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    pe_ratio: Optional[float] = None
    eps: Optional[float] = None
    revenue_growth: Optional[float] = None
    debt_to_equity: Optional[float] = None
    roe: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None

class HistoricalPoint(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int

class TechnicalIndicators(BaseModel):
    rsi: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    ma20: Optional[float] = None
    ma50: Optional[float] = None
    ma100: Optional[float] = None
    ma200: Optional[float] = None
    bb_high: Optional[float] = None
    bb_low: Optional[float] = None
    atr: Optional[float] = None
    vwap: Optional[float] = None
    stoch_rsi: Optional[float] = None
    adx: Optional[float] = None
    trend: str = "Neutral"
    support: List[float] = []
    resistance: List[float] = []
    signals: List[str] = []
