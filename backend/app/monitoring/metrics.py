from prometheus_client import Counter, Histogram
import time
from starlette.middleware.base import BaseHTTPMiddleware

# Prometheus Metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        method = request.method
        endpoint = request.url.path
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            status_code = str(response.status_code)
            
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - start_time)
            
            return response
        except Exception as e:
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status="500").inc()
            raise e
