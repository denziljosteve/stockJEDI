import json
from typing import Dict, Any

class PromptBuilder:
    @staticmethod
    def build_investment_report_prompt(data: Dict[str, Any]) -> str:
        """
        Build a structured prompt for the AI report.
        """
        return f"""
Analyze the following stock data and provide a comprehensive institutional-grade investment report.

STOCK DATA (JSON):
{json.dumps(data, indent=2)}

INSTRUCTIONS:
You are an expert institutional equity analyst. Provide a detailed analysis including:
1. Company Overview: Business model and market position.
2. Financial Health Assessment: Analysis of key metrics (PE, EPS, ROE, etc.).
3. Technical Analysis Summary: Interpretation of RSI, MACD, and trends.
4. Strengths: Core advantages.
5. Weaknesses: Internal vulnerabilities.
6. Key Risks: External threats and market risks.
7. Growth Outlook: Short-term and long-term prospects.
8. Competitor Observations: How they stand against peers.
9. Market Sentiment Interpretation: News and social sentiment analysis.
10. Investment Thesis: Your logical reasoning for the stock's future.
11. Buy/Hold/Sell Recommendation: Clear actionable advice.
12. Confidence Level: High/Medium/Low.

CONSTRAINTS:
- Do NOT generate specific price targets or price predictions.
- Be objective and data-driven.
- Use professional financial terminology.
"""

    @staticmethod
    def get_system_prompt() -> str:
        return "You are a professional equity research analyst working for a top-tier investment bank. Your goal is to provide objective, data-driven, and insightful stock analysis."
