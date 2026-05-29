from typing import Dict, Any

class ScoringEngine:
    @staticmethod
    def calculate_overall_score(
        fundamentals_score: float, # 0-100
        technical_score: float,    # 0-100
        sentiment_score: float,    # 0-100
        growth_score: float,       # 0-100
        risk_score: float          # 0-100 (inverse, higher means lower risk)
    ) -> Dict[str, Any]:
        """
        Weights:
        Fundamentals = 35%
        Technical = 25%
        Sentiment = 15%
        Growth = 15%
        Risk = 10%
        """
        weights = {
            "fundamentals": 0.35,
            "technical": 0.25,
            "sentiment": 0.15,
            "growth": 0.15,
            "risk": 0.10
        }

        overall_score = (
            fundamentals_score * weights["fundamentals"] +
            technical_score * weights["technical"] +
            sentiment_score * weights["sentiment"] +
            growth_score * weights["growth"] +
            risk_score * weights["risk"]
        )

        recommendation = "Hold"
        if overall_score > 80:
            recommendation = "Strong Buy"
        elif overall_score > 65:
            recommendation = "Buy"
        elif overall_score < 30:
            recommendation = "Strong Sell"
        elif overall_score < 45:
            recommendation = "Sell"

        confidence = "Medium"
        if overall_score > 85 or overall_score < 15:
            confidence = "High"
        elif 40 < overall_score < 60:
            confidence = "Low"

        return {
            "overall_score": round(overall_score, 2),
            "recommendation": recommendation,
            "confidence": confidence,
            "breakdown": {
                "fundamentals": fundamentals_score,
                "technical": technical_score,
                "sentiment": sentiment_score,
                "growth": growth_score,
                "risk": risk_score
            }
        }

    @staticmethod
    def normalize_technical_score(indicators: Dict[str, Any]) -> float:
        # Simple normalization logic
        score = 50 # Start neutral
        trend = indicators.get("trend", "Neutral")
        rsi = indicators.get("rsi", 50)
        
        if trend == "Bullish": score += 20
        if trend == "Bearish": score -= 20
        
        if 40 < rsi < 60: score += 10
        elif rsi > 70: score -= 10 # Overbought
        elif rsi < 30: score += 15 # Oversold
        
        return max(0, min(100, score))

    @staticmethod
    def normalize_sentiment_score(sentiment: float) -> float:
        # sentiment is -100 to 100
        # normalize to 0 to 100
        return (sentiment + 100) / 2
