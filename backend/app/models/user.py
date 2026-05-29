from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    watchlists = relationship("Watchlist", back_populates="user")
    portfolios = relationship("Portfolio", back_populates="user")

class Watchlist(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    ticker = Column(String, index=True, nullable=False)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="watchlists")

class Portfolio(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    ticker = Column(String, index=True, nullable=False)
    shares = Column(Float, default=0.0)
    average_buy_price = Column(Float, default=0.0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="portfolios")
    transactions = relationship("PortfolioTransaction", back_populates="portfolio")

class PortfolioTransaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolio.id"))
    transaction_type = Column(String) # "BUY" or "SELL"
    shares = Column(Float, nullable=False)
    price_per_share = Column(Float, nullable=False)
    executed_at = Column(DateTime(timezone=True), server_default=func.now())

    portfolio = relationship("Portfolio", back_populates="transactions")
