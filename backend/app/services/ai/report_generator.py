from typing import Dict, Any
from app.services.market.aggregator import MarketAggregator
from app.services.sentiment.news_analyzer import NewsAnalyzer
from app.services.sentiment.social_analyst_analyzer import RedditAnalyzer, AnalystAnalyzer
from app.services.sentiment.sentiment_engine import sentiment_engine
from app.services.ai.groq_client import groq_client
from app.services.ai.prompt_builder import PromptBuilder
from app.services.ai.scoring_engine import ScoringEngine
from loguru import logger

class ReportGenerator:
    @staticmethod
    async def generate_full_report(ticker: str) -> Dict[str, Any]:
        """
        1. Fetch market data
        2. Fetch sentiment data
        3. Calculate scores
        4. Generate AI report
        """
        # 1. Market Data
        market_data = await MarketAggregator.get_comprehensive_data(ticker)
        if "error" in market_data:
            return market_data

        # 2. Sentiment Data
        news_entries = await NewsAnalyzer.fetch_news(ticker)
        reddit_entries = await RedditAnalyzer.fetch_discussions(ticker)
        analyst_entries = await AnalystAnalyzer.fetch_ratings(ticker)
        
        all_sentiment_entries = news_entries + reddit_entries + analyst_entries
        sentiment_result = sentiment_engine.aggregate_sentiment(all_sentiment_entries)

        # 3. Calculate Scores
        tech_score = ScoringEngine.normalize_technical_score(market_data["indicators"])
        sent_score = ScoringEngine.normalize_sentiment_score(sentiment_result.overall_sentiment)
        
        # Mock growth and risk for now
        growth_score = 70.0 
        risk_score = 60.0 # 60/100 (Moderate risk)

        final_scoring = ScoringEngine.calculate_overall_score(
            fundamentals_score=75.0, # Mock fundamental score
            technical_score=tech_score,
            sentiment_score=sent_score,
            growth_score=growth_score,
            risk_score=risk_score
        )

        # 4. Generate AI Report
        report_data = {
            "company": market_data["info"],
            "financials": market_data["info"], # Simplified for prompt
            "technicalIndicators": market_data["indicators"],
            "sentiment": sentiment_result.dict(),
            "scoring": final_scoring
        }
        
        prompt = PromptBuilder.build_investment_report_prompt(report_data)
        system_prompt = PromptBuilder.get_system_prompt()
        
        ai_report_content = await groq_client.generate_completion(prompt, system_prompt)

        return {
            "ticker": ticker,
            "market_data": market_data,
            "sentiment": sentiment_result.dict(),
            "scoring": final_scoring,
            "report_content": ai_report_content
        }
