from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class PredictionBase(BaseModel):
    ticker: str
    horizon: str  # 1d, 1w, 1m, 3m, 6m, 1y
    bullish_probability: float
    bearish_probability: float
    neutral_probability: float
    confidence: float

class Prediction(PredictionBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True

class AnalysisBase(BaseModel):
    ticker: str
    fundamental_score: float
    technical_score: float
    sentiment_score: float
    growth_score: float
    risk_score: float
    overall_score: float
    recommendation: str

class Analysis(AnalysisBase):
    id: Optional[int] = None
    ai_report: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
