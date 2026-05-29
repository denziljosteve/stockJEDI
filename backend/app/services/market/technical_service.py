import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator, StochRSIIndicator
from ta.trend import MACD, ADXIndicator, SMAIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from typing import Dict, Any, List
from app.schemas.market_data import TechnicalIndicators

class TechnicalAnalysisService:
    @staticmethod
    def calculate_indicators(df: pd.DataFrame) -> TechnicalIndicators:
        if df.empty or len(df) < 50: # Minimum data for basic indicators
            return TechnicalIndicators()

        close = df['Close']
        high = df['High']
        low = df['Low']
        volume = df['Volume']

        # Momentum
        rsi = RSIIndicator(close=close).rsi().iloc[-1]
        stoch_rsi = StochRSIIndicator(close=close).stochrsi().iloc[-1]

        # Trend
        macd_obj = MACD(close=close)
        macd = macd_obj.macd().iloc[-1]
        macd_signal = macd_obj.macd_signal().iloc[-1]
        
        adx = ADXIndicator(high=high, low=low, close=close).adx().iloc[-1]
        
        ma20 = SMAIndicator(close=close, window=20).sma_indicator().iloc[-1]
        ma50 = SMAIndicator(close=close, window=50).sma_indicator().iloc[-1]
        ma100 = SMAIndicator(close=close, window=100).sma_indicator().iloc[-1] if len(df) >= 100 else None
        ma200 = SMAIndicator(close=close, window=200).sma_indicator().iloc[-1] if len(df) >= 200 else None

        # Volatility
        bb = BollingerBands(close=close)
        bb_high = bb.bollinger_hband().iloc[-1]
        bb_low = bb.bollinger_lband().iloc[-1]
        
        atr = AverageTrueRange(high=high, low=low, close=close).average_true_range().iloc[-1]

        # VWAP (Simplified calculation if intraday data is not available)
        vwap = (volume * (high + low + close) / 3).sum() / volume.sum()

        # Trend Detection
        trend = "Neutral"
        if ma50 and close.iloc[-1] > ma50:
            trend = "Bullish"
        elif ma50 and close.iloc[-1] < ma50:
            trend = "Bearish"

        # Support/Resistance (Simple peak/trough detection)
        support = [low.min(), low.rolling(window=20).min().iloc[-1]]
        resistance = [high.max(), high.rolling(window=20).max().iloc[-1]]

        # Signals
        signals = []
        if rsi > 70:
            signals.append("Overbought")
        elif rsi < 30:
            signals.append("Oversold")
        
        if macd > macd_signal:
            signals.append("MACD Bullish Cross")
        elif macd < macd_signal:
            signals.append("MACD Bearish Cross")

        return TechnicalIndicators(
            rsi=float(rsi),
            macd=float(macd),
            macd_signal=float(macd_signal),
            ma20=float(ma20),
            ma50=float(ma50),
            ma100=float(ma100) if ma100 else None,
            ma200=float(ma200) if ma200 else None,
            bb_high=float(bb_high),
            bb_low=float(bb_low),
            atr=float(atr),
            vwap=float(vwap),
            stoch_rsi=float(stoch_rsi),
            adx=float(adx),
            trend=trend,
            support=list(set([float(s) for s in support])),
            resistance=list(set([float(r) for r in resistance])),
            signals=signals
        )
