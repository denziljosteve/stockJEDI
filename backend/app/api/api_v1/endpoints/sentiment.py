from typing import Any
from fastapi import APIRouter
from app.services.sentiment.news_analyzer import NewsAnalyzer
from app.services.sentiment.social_analyst_analyzer import RedditAnalyzer, AnalystAnalyzer
from app.services.sentiment.sentiment_engine import sentiment_engine

router = APIRouter()

@router.post("/{ticker}", response_model=dict)
async def get_stock_sentiment(ticker: str) -> Any:
    """
    Get aggregated sentiment for a stock from news and social media.
    """
    news_entries = await NewsAnalyzer.fetch_news(ticker)
    reddit_entries = await RedditAnalyzer.fetch_discussions(ticker)
    analyst_entries = await AnalystAnalyzer.fetch_ratings(ticker)
    
    all_entries = news_entries + reddit_entries + analyst_entries
    result = sentiment_engine.aggregate_sentiment(all_entries)
    
    return {
        "ticker": ticker,
        "sentiment": result.dict(),
        "entries_count": len(all_entries)
    }
