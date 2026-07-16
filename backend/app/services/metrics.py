"""
Career-Ops Prometheus Metrics
Exposes application metrics for Prometheus scraping.
"""

import time
from functools import wraps

from prometheus_client import Counter, Gauge, Histogram, generate_latest

# ── HTTP Request Metrics ──────────────────────────────────────────────

HTTP_REQUESTS_TOTAL = Counter(
    "careerops_http_requests_total",
    "Total HTTP requests",
    labelnames=["method", "endpoint", "status"],
)

HTTP_REQUEST_DURATION = Histogram(
    "careerops_http_request_duration_seconds",
    "HTTP request duration in seconds",
    labelnames=["method", "endpoint"],
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

ACTIVE_REQUESTS = Gauge(
    "careerops_http_active_requests",
    "Currently active HTTP requests",
)

# ── Database Metrics ──────────────────────────────────────────────────

DB_CONNECTION_POOL_SIZE = Gauge(
    "careerops_db_connection_pool_size",
    "Current database connection pool size",
)

DB_QUERY_DURATION = Histogram(
    "careerops_db_query_duration_seconds",
    "Database query duration in seconds",
    labelnames=["operation"],
    buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 2.0),
)

# ── Business Metrics ──────────────────────────────────────────────────

USERS_TOTAL = Gauge(
    "careerops_users_total",
    "Total number of registered users",
)

JOBS_TOTAL = Gauge(
    "careerops_jobs_total",
    "Total number of jobs tracked",
)

APPLICATIONS_TOTAL = Gauge(
    "careerops_applications_total",
    "Total number of job applications",
)

APPLICATIONS_BY_STATUS = Gauge(
    "careerops_applications_by_status",
    "Applications grouped by status",
    labelnames=["status"],
)

RESUMES_TOTAL = Gauge(
    "careerops_resumes_total",
    "Total number of uploaded resumes",
)

AI_REQUESTS_TOTAL = Counter(
    "careerops_ai_requests_total",
    "Total AI feature requests",
    labelnames=["feature"],
)

AI_REQUEST_DURATION = Histogram(
    "careerops_ai_request_duration_seconds",
    "AI request duration in seconds",
    labelnames=["feature"],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0),
)

# ── System Metrics ────────────────────────────────────────────────────

APP_INFO = Gauge(
    "careerops_app_info",
    "Application metadata",
    labelnames=["version", "env"],
)
APP_INFO.labels(version="0.1.0", env="production").set(1)

UP = Gauge("careerops_up", "Application is up and running")
UP.set(1)


def get_metrics():
    """Return the latest Prometheus metrics as bytes."""
    return generate_latest()


def track_request_metrics(method: str, endpoint: str, status: int, duration: float):
    """Record metrics for a completed HTTP request."""
    HTTP_REQUESTS_TOTAL.labels(method=method, endpoint=endpoint, status=str(status)).inc()
    HTTP_REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)


def track_ai_request(feature: str):
    """Decorator to track AI request metrics."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = await func(*args, **kwargs) if hasattr(func, "__code__") else func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start
                AI_REQUESTS_TOTAL.labels(feature=feature).inc()
                AI_REQUEST_DURATION.labels(feature=feature).observe(duration)

        return wrapper

    return decorator
