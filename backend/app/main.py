from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from loguru import logger
from prometheus_client import make_asgi_app

from app.api.api_v1.api import api_router
from app.api.websockets import router as websocket_router
from app.core.config import settings
from app.middleware.error_handler import ErrorHandlingMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limit import setup_rate_limit
from app.monitoring.metrics import PrometheusMiddleware
from app.core.config_validator import validate_config

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Rate Limiter
setup_rate_limit(app)

# Prometheus Metrics Middleware
app.add_middleware(PrometheusMiddleware)

# Prometheus Endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Custom Middlewares
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(LoggingMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(websocket_router, tags=["websockets"])

@app.on_event("startup")
async def startup_event():
    # Validate environment variables before starting
    validate_config()
    logger.info("Starting up stockJEDI backend...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down stockJEDI backend...")
