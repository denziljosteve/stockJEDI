import pytest
import numpy as np
import pandas as pd

# Add root project path to allow importing ml module from tests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ml.features.feature_pipeline import feature_pipeline
from ml.models.ensemble_model import ensemble_model
from backend.app.services.prediction.prediction_service import prediction_service

def test_feature_pipeline():
    dates = pd.date_range(start="2023-01-01", periods=200)
    hist_data = {
        'Open': [100 + i for i in range(200)],
        'High': [105 + i for i in range(200)],
        'Low': [95 + i for i in range(200)],
        'Close': [102 + i for i in range(200)],
        'Volume': [1000 for _ in range(200)]
    }
    df = pd.DataFrame(hist_data, index=dates)
    
    market_data = {
        "info": {"pe_ratio": 20, "eps": 2, "market_cap": 1e9},
        "sentiment": {"overall_sentiment": 50.0}
    }
    
    features_df = feature_pipeline.generate_features(market_data, df)
    
    assert not features_df.empty
    assert "PE" in features_df.columns
    assert "RSI" in features_df.columns
    assert "News_sentiment" in features_df.columns
    assert "Reddit_sentiment" in features_df.columns
    assert "Analyst_sentiment" in features_df.columns

def test_ensemble_model():
    dummy_features = np.random.rand(1, 15)
    
    result = ensemble_model.predict_probabilities(dummy_features, 7)
    
    assert "bullish" in result
    assert "bearish" in result
    assert "neutral" in result
    assert 99.0 <= (result["bullish"] + result["bearish"] + result["neutral"]) <= 101.0

def test_prediction_service_signals():
    market_data = {
        "indicators": {"trend": "Bullish", "rsi": 80}
    }
    pred = {"bullish": 60, "bearish": 30}
    
    signals = prediction_service._generate_signals(market_data, pred)
    assert any("Bullish" in s or "uptrend" in s.lower() for s in signals)
    assert any("overbought" in s.lower() for s in signals)
