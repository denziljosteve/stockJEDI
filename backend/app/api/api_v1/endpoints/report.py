from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.stock import Stock as StockModel, Analysis
from app.services.ai.report_generator import ReportGenerator

router = APIRouter()


@router.post("/{ticker}", response_model=dict)
async def generate_report(ticker: str, current_user: dict = Depends(get_current_user)) -> Any:
    report = await ReportGenerator.generate_full_report(ticker)
    return report


@router.get("/{ticker}", response_model=dict)
def get_report(
    ticker: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    stock = db.query(StockModel).filter(StockModel.ticker == ticker.upper()).first()
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report for {ticker.upper()} not found.",
        )

    analysis = (
        db.query(Analysis)
        .filter(Analysis.stock_id == stock.id)
        .order_by(Analysis.created_at.desc())
        .first()
    )
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No analysis found for {ticker.upper()}.",
        )

    return {
        "ticker": ticker.upper(),
        "report": {
            "id": analysis.id,
            "fundamental_score": analysis.fundamental_score,
            "technical_score": analysis.technical_score,
            "sentiment_score": analysis.sentiment_score,
            "growth_score": analysis.growth_score,
            "risk_score": analysis.risk_score,
            "overall_score": analysis.overall_score,
            "recommendation": analysis.recommendation,
            "ai_report": analysis.ai_report,
            "created_at": str(analysis.created_at) if analysis.created_at else None,
        },
    }
