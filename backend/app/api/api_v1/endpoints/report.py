from typing import Any
from fastapi import APIRouter

from app.services.ai.report_generator import ReportGenerator

router = APIRouter()

@router.post("/{ticker}", response_model=dict)
async def generate_report(ticker: str) -> Any:
    """
    Generate a detailed AI investment report for a stock.
    """
    report = await ReportGenerator.generate_full_report(ticker)
    return report

@router.get("/{ticker}", response_model=dict)
def get_report(ticker: str) -> Any:
    """
    Get detailed AI report for a stock.
    """
    return {"ticker": ticker, "report": "Institutional grade report content..."}
