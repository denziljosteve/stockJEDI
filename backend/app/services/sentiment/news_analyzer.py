import yfinance as yf
from typing import List
from datetime import datetime
from loguru import logger

from app.services.sentiment.sentiment_engine import SentimentEntry, sentiment_engine


class NewsAnalyzer:
    @staticmethod
    async def fetch_news(ticker: str) -> List[SentimentEntry]:
        """
        Fetch news using yfinance as a free real data source.
        """
        entries = []
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            
            for item in news:
                # yfinance news items have 'title', 'publisher', 'providerPublishTime', 'relatedTickers'
                title = item.get('title', '')
                publisher = item.get('publisher', 'Unknown')
                pub_time = item.get('providerPublishTime')
                published_at = datetime.fromtimestamp(pub_time).isoformat() if pub_time else datetime.now().isoformat()
                
                # We analyze the title as the content is often just a link
                analysis = sentiment_engine.analyze_text(title)
                entries.append(SentimentEntry(
                    source=publisher,
                    title=title,
                    content=item.get('link', ''), # Use link as content
                    published_at=published_at,
                    sentiment_score=analysis["score"],
                    sentiment_label=analysis["label"]
                ))
        except Exception as e:
            logger.error(f"Error fetching real news for {ticker}: {e}")
            
        return entries
