from typing import List, Dict, Any
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

class SentimentResult(BaseModel):
    positive_score: float
    negative_score: float
    neutral_score: float
    overall_sentiment: float  # -100 to 100
    confidence: float
    summary: str

class SentimentEntry(BaseModel):
    source: str
    title: str
    content: str
    published_at: str
    sentiment_score: float
    sentiment_label: str

class SentimentEngine:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze a single piece of text and return scores.
        """
        if not text:
            return {"score": 0, "label": "Neutral"}
        
        vader_scores = self.analyzer.polarity_scores(text)
        compound = vader_scores['compound'] # -1 to 1
        
        # Normalize to -100 to 100
        score = compound * 100
        
        label = "Neutral"
        if score > 20:
            label = "Bullish"
        elif score < -20:
            label = "Bearish"
            
        return {
            "score": score,
            "label": label,
            "vader": vader_scores
        }

    def aggregate_sentiment(self, entries: List[SentimentEntry]) -> SentimentResult:
        if not entries:
            return SentimentResult(
                positive_score=0, negative_score=0, neutral_score=0,
                overall_sentiment=0, confidence=0, summary="No sentiment data available."
            )

        total_score = sum(e.sentiment_score for e in entries)
        avg_score = total_score / len(entries)
        
        pos = len([e for e in entries if e.sentiment_label == "Bullish"])
        neg = len([e for e in entries if e.sentiment_label == "Bearish"])
        neu = len(entries) - pos - neg

        return SentimentResult(
            positive_score=(pos / len(entries)) * 100,
            negative_score=(neg / len(entries)) * 100,
            neutral_score=(neu / len(entries)) * 100,
            overall_sentiment=avg_score,
            confidence=min(len(entries) / 10, 1.0), # Higher confidence with more entries
            summary=f"Analyzed {len(entries)} sources. Majority sentiment is {self._get_label(avg_score)}."
        )

    def _get_label(self, score: float) -> str:
        if score > 20: return "Bullish"
        if score < -20: return "Bearish"
        return "Neutral"

sentiment_engine = SentimentEngine()
