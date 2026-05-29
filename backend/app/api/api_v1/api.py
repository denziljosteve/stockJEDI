from fastapi import APIRouter

from app.api.api_v1.endpoints import health, stock, prediction, report, sentiment, portfolio, watchlist

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(stock.router, prefix="/stock", tags=["stock"])
api_router.include_router(prediction.router, prefix="/prediction", tags=["prediction"])
api_router.include_router(report.router, prefix="/report", tags=["report"])
api_router.include_router(sentiment.router, prefix="/sentiment", tags=["sentiment"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(watchlist.router, prefix="/watchlist", tags=["watchlist"])
