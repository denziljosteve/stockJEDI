import pandas as pd
import pytest
from app.services.market.technical_service import TechnicalAnalysisService

@pytest.fixture
def sample_df():
    # Create 200 days of sample data
    dates = pd.date_range(start="2023-01-01", periods=200)
    data = {
        'Open': [100 + i for i in range(200)],
        'High': [105 + i for i in range(200)],
        'Low': [95 + i for i in range(200)],
        'Close': [102 + i for i in range(200)],
        'Volume': [1000 for _ in range(200)]
    }
    df = pd.DataFrame(data, index=dates)
    return df

def test_calculate_indicators(sample_df):
    indicators = TechnicalAnalysisService.calculate_indicators(sample_df)
    
    assert indicators.rsi is not None
    assert indicators.macd is not None
    assert indicators.ma50 is not None
    assert indicators.trend in ["Bullish", "Bearish", "Neutral"]
    assert len(indicators.support) > 0
    assert len(indicators.resistance) > 0
