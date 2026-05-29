from app.services.ai.scoring_engine import ScoringEngine
from app.services.sentiment.sentiment_engine import sentiment_engine, SentimentEntry

def test_scoring_engine_weights():
    # Test perfect scores
    result = ScoringEngine.calculate_overall_score(100, 100, 100, 100, 100)
    assert result["overall_score"] == 100.0
    assert result["recommendation"] == "Strong Buy"
    
    # Test neutral scores
    result = ScoringEngine.calculate_overall_score(50, 50, 50, 50, 50)
    assert result["overall_score"] == 50.0
    assert result["recommendation"] == "Hold"

def test_sentiment_analysis():
    bullish_text = "The stock is going to moon, amazing earnings and great future!"
    analysis = sentiment_engine.analyze_text(bullish_text)
    assert analysis["score"] > 0
    assert analysis["label"] == "Bullish"
    
    bearish_text = "Disastrous results, bankruptcy imminent, sell everything."
    analysis = sentiment_engine.analyze_text(bearish_text)
    assert analysis["score"] < 0
    assert analysis["label"] == "Bearish"

def test_sentiment_aggregation():
    entries = [
        SentimentEntry(source="test", title="good", content="good", published_at="now", sentiment_score=80, sentiment_label="Bullish"),
        SentimentEntry(source="test", title="bad", content="bad", published_at="now", sentiment_score=-80, sentiment_label="Bearish")
    ]
    result = sentiment_engine.aggregate_sentiment(entries)
    assert result.overall_sentiment == 0
    assert result.neutral_score == 0
    assert result.positive_score == 50
    assert result.negative_score == 50
