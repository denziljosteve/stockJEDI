import pandas as pd
import numpy as np
from typing import Dict, Any

class FeaturePipeline:
    @staticmethod
    def generate_features(market_data: Dict[str, Any], historical_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate a feature set for model prediction.
        
        market_data: Data from MarketAggregator
        historical_df: Dataframe of historical prices
        """
        if historical_df.empty:
            return pd.DataFrame()
            
        df = historical_df.copy()
        
        from ta.momentum import RSIIndicator
        from ta.trend import MACD, SMAIndicator
        from ta.volatility import AverageTrueRange

        df['RSI'] = RSIIndicator(close=df['Close'], window=14).rsi()
        macd_obj = MACD(close=df['Close'])
        df['MACD'] = macd_obj.macd()
        df['MA20'] = SMAIndicator(close=df['Close'], window=20).sma_indicator()
        df['MA50'] = SMAIndicator(close=df['Close'], window=50).sma_indicator()
        df['MA100'] = SMAIndicator(close=df['Close'], window=100).sma_indicator()
        df['MA200'] = SMAIndicator(close=df['Close'], window=200).sma_indicator()
        df['ATR'] = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'], window=14).average_true_range()

        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        df['VWAP'] = (typical_price * df['Volume']).rolling(20).sum() / df['Volume'].rolling(20).sum()

        from ta.trend import ADXIndicator
        df['ADX'] = ADXIndicator(high=df['High'], low=df['Low'], close=df['Close'], window=14).adx()

        # Financial Features
        info = market_data.get('info', {})
        df['PE'] = info.get('pe_ratio', 15.0)
        df['EPS'] = info.get('eps', 5.0)
        df['Revenue_growth'] = info.get('revenue_growth', 0.05)
        df['ROE'] = info.get('return_on_equity', 0.1)
        df['Debt_Equity'] = info.get('debt_to_equity', 50.0)

        # Sentiment features - neutral defaults matching data_collector.py schema
        df['News_sentiment'] = 0.0
        df['Reddit_sentiment'] = 0.0
        df['Analyst_sentiment'] = 0.0
        
        # Target variable (e.g. 1 week future return)
        df['Target_1w'] = df['Close'].shift(-5) / df['Close'] - 1.0
        
        return df.dropna()

feature_pipeline = FeaturePipeline()
