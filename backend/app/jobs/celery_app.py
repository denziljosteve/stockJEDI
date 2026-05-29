from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "stockjedi_jobs",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.task_routes = {
    "app.jobs.price_updater.*": {"queue": "prices"},
    "app.jobs.historical_sync.*": {"queue": "historical"},
}

@celery_app.task
def update_stock_prices():
    """
    Background job to update prices for all active stocks.
    """
    # Logic to fetch tickers from DB and update them
    pass

@celery_app.task
def sync_historical_data(ticker: str):
    """
    Background job to sync historical data for a specific ticker.
    """
    pass
