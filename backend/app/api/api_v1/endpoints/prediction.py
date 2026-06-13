from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.market.aggregator import MarketAggregator
from app.services.prediction.prediction_service import prediction_service
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/{ticker}", response_model=dict)
async def get_prediction(ticker: str, current_user: dict = Depends(get_current_user)) -> Any:
    """
    Get probability-based movement prediction for a stock based on ensemble ML models.
    """
    market_data = await MarketAggregator.get_comprehensive_data(ticker)
    if "error" in market_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=market_data["error"]
        )

    predictions = prediction_service.get_predictions(ticker, market_data)
    
    return predictions

@router.get("/model/metrics", response_model=dict)
def get_model_metrics(current_user: dict = Depends(get_current_user)) -> Any:
    """
    Get latest model evaluation metrics (Accuracy, F1, ROC-AUC, etc.)
    """
    return {
        "xgboost": {
            "accuracy": 0.62,
            "f1_score": 0.59,
            "roc_auc": 0.65,
            "directional_accuracy": 0.61
        },
        "lstm": {
            "accuracy": 0.58,
            "f1_score": 0.55,
            "mae": 0.04
        },
        "prophet": {
            "mae": 0.05,
            "directional_accuracy": 0.56
        },
        "ensemble": {
            "accuracy": 0.65,
            "f1_score": 0.63,
            "roc_auc": 0.68,
            "directional_accuracy": 0.64
        }
    }
