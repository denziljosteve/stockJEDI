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
        
        # In a real implementation, we would calculate all these features based on historical_df
        # For now, we extract available indicators from market_data if we only need a single row
        # If we need a historical dataset to train, we'd apply TA lib across historical_df
        
        # Dummy mock features for demonstration
        df['RSI'] = np.random.uniform(30, 70, size=len(df))
        df['MACD'] = np.random.normal(0, 1, size=len(df))
        df['MA50'] = df['Close'].rolling(window=50).mean()
        df['MA200'] = df['Close'].rolling(window=200).mean()
        
        # Financial Features
        info = market_data.get('info', {})
        df['PE'] = info.get('pe_ratio', 15.0)
        df['EPS'] = info.get('eps', 5.0)
        df['Market_Cap'] = info.get('market_cap', 1e10)
        
        # Sentiment Features
        sentiment = market_data.get('sentiment', {})
        df['Sentiment_Score'] = sentiment.get('overall_sentiment', 0.0)
        
        # Target variable (e.g. 1 week future return)
        df['Target_1w'] = df['Close'].shift(-5) / df['Close'] - 1.0
        
        return df.dropna()

feature_pipeline = FeaturePipeline()
