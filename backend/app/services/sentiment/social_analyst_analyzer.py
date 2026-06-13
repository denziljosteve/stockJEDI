import yfinance as yf
from typing import List
from datetime import datetime
from loguru import logger

from app.services.sentiment.sentiment_engine import SentimentEntry, sentiment_engine


class RedditAnalyzer:
    @staticmethod
    async def fetch_discussions(ticker: str) -> List[SentimentEntry]:
        # Since Reddit requires OAuth and API keys, we fallback to a simulated realistic sentiment
        # to ensure the pipeline functions structurally.
        # In a real environment, PRAW would be used here.
        entries = []
        analysis = sentiment_engine.analyze_text(f"{ticker} has strong potential based on latest earnings.")
        entries.append(SentimentEntry(
            source="r/WallStreetBets (Simulated)",
            title=f"{ticker} Discussion",
            content="Simulated Reddit discussion data due to missing API keys.",
            published_at=datetime.now().isoformat(),
            sentiment_score=analysis["score"],
            sentiment_label=analysis["label"]
        ))
        return entries


class AnalystAnalyzer:
    @staticmethod
    async def fetch_ratings(ticker: str) -> List[SentimentEntry]:
        entries = []
        try:
            stock = yf.Ticker(ticker)
            recs = stock.upgrades_downgrades
            
            if recs is not None and not recs.empty:
                # Get the last 5 recommendations
                recent_recs = recs.tail(5)
                for index, row in recent_recs.iterrows():
                    firm = row.get('Firm', 'Unknown Firm')
                    to_grade = row.get('ToGrade', '')
                    action = row.get('Action', '')
                    
                    text = f"{firm} {action} {ticker} to {to_grade}"
                    analysis = sentiment_engine.analyze_text(text)
                    
                    entries.append(SentimentEntry(
                        source=firm,
                        title=text,
                        content=text,
                        published_at=str(index),
                        sentiment_score=analysis["score"],
                        sentiment_label=analysis["label"]
                    ))
        except Exception as e:
            logger.error(f"Error fetching analyst ratings for {ticker}: {e}")
            
        return entries
