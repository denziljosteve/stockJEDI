from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class Stock(Base):
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True)
    source = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    analyses = relationship("Analysis", back_populates="stock")
    predictions = relationship("Prediction", back_populates="stock")

class Analysis(Base):
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stock.id"))
    fundamental_score = Column(Float)
    technical_score = Column(Float)
    sentiment_score = Column(Float)
    growth_score = Column(Float)
    risk_score = Column(Float)
    overall_score = Column(Float)
    recommendation = Column(String)
    ai_report = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    stock = relationship("Stock", back_populates="analyses")

class Prediction(Base):
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stock.id"))
    horizon = Column(String)
    bullish_probability = Column(Float)
    bearish_probability = Column(Float)
    neutral_probability = Column(Float)
    confidence = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    stock = relationship("Stock", back_populates="predictions")
