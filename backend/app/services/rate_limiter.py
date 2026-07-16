"""
Rate Limiting Middleware for Career-Ops API Protection.
Implements token bucket algorithm with per-user and per-IP limits.

Configuration via environment variables:
- RATE_LIMIT_ENABLED: Enable/disable rate limiting (default: true)
- RATE_LIMIT_DEFAULT: Default requests per minute (default: 60)
- RATE_LIMIT_AI: AI endpoint requests per minute (default: 10)
- RATE_LIMIT_AUTH: Auth endpoint requests per minute (default: 20)
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from collections.abc import Callable

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from backend.app.core.config import settings

logger = logging.getLogger(__name__)

# ── Configuration ──────────────────────────────────────────────────────

RATE_LIMIT_ENABLED: bool = settings.APP_ENV.lower() in ("production", "staging")
RATE_LIMIT_DEFAULT: int = 60    # requests per minute
RATE_LIMIT_AUTH: int = 20       # login/register per minute
RATE_LIMIT_AI: int = 10         # AI endpoint calls per minute
WINDOW_SIZE: float = 60.0       # sliding window in seconds


# ── Token Bucket ──────────────────────────────────────────────────────


class TokenBucket:
    """Sliding window token bucket rate limiter."""

    def __init__(self, capacity: int, window: float = WINDOW_SIZE) -> None:
        self.capacity = capacity
        self.window = window
        self.tokens: dict[str, list[float]] = defaultdict(list)

    def consume(self, key: str, cost: int = 1) -> bool:
        """
        Try to consume `cost` tokens for `key`.
        Returns True if allowed, False if rate limited.
        """
        now = time.time()
        cutoff = now - self.window

        # Get timestamps for this key
        timestamps = self.tokens[key]

        # Remove expired timestamps
        self.tokens[key] = [t for t in timestamps if t > cutoff]

        # Check if within capacity
        if len(self.tokens[key]) + cost <= self.capacity:
            for _ in range(cost):
                self.tokens[key].append(now)
            return True

        return False

    def remaining(self, key: str) -> int:
        """Get remaining tokens for key."""
        now = time.time()
        cutoff = now - self.window
        self.tokens[key] = [t for t in self.tokens[key] if t > cutoff]
        return max(0, self.capacity - len(self.tokens[key]))  # type: ignore[no-any-return]


# ── Middleware ──────────────────────────────────────────────────────────

# Global rate limiter instances
_default_limiter = TokenBucket(RATE_LIMIT_DEFAULT)
_auth_limiter = TokenBucket(RATE_LIMIT_AUTH)
_ai_limiter = TokenBucket(RATE_LIMIT_AI)


def _get_rate_limit_key(request: Request) -> tuple[str, TokenBucket, int]:
    """
    Determine the rate limit key and applicable bucket for a request.

    Returns: (key, limiter, limit_per_minute)
    """
    # Use user ID if authenticated, otherwise IP
    user_id = getattr(request.state, "user_id", None)
    ip = request.client.host if request.client else "unknown"
    key = f"user:{user_id}" if user_id else f"ip:{ip}"

    # Determine limiter based on path
    path = request.url.path.lower()

    if "/auth/" in path or "/users/register" in path:
        return key, _auth_limiter, RATE_LIMIT_AUTH
    elif "/ai/" in path:
        return key, _ai_limiter, RATE_LIMIT_AI
    else:
        return key, _default_limiter, RATE_LIMIT_DEFAULT


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for rate limiting.

    Adds headers:
    - X-RateLimit-Limit: Max requests per window
    - X-RateLimit-Remaining: Remaining requests in window
    - X-RateLimit-Reset: Seconds until window resets
    - Retry-After: Seconds to wait (when 429)
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting when disabled
        if not RATE_LIMIT_ENABLED:
            return await call_next(request)

        # Skip static files, docs, and metrics
        path = request.url.path
        if any(
            path.startswith(p)
            for p in ["/static", "/docs", "/openapi.json", "/metrics", "/health", "/ready", "/live"]
        ):
            return await call_next(request)

        try:
            key, limiter, limit = _get_rate_limit_key(request)

            if not limiter.consume(key):
                remaining = limiter.remaining(key)
                wait_time = int(WINDOW_SIZE)

                logger.warning("Rate limit exceeded: %s (path=%s)", key, path)

                return JSONResponse(
                    status_code=429,
                    content={
                        "success": False,
                        "message": "Too many requests. Please slow down.",
                        "data": {
                            "retry_after_seconds": wait_time,
                            "limit": limit,
                            "remaining": remaining,
                        },
                    },
                    headers={
                        "X-RateLimit-Limit": str(limit),
                        "X-RateLimit-Remaining": str(remaining),
                        "X-RateLimit-Reset": str(wait_time),
                        "Retry-After": str(wait_time),
                        "Access-Control-Expose-Headers": (
                            "X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After"
                        ),
                    },
                )

            # Add rate limit headers to response
            response = await call_next(request)
            remaining = limiter.remaining(key)
            response.headers["X-RateLimit-Limit"] = str(limit)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(int(WINDOW_SIZE))
            return response

        except Exception as e:
            logger.error("Rate limiter error: %s", e)
            # Fail open — allow request if rate limiter itself fails
            return await call_next(request)


# ── Factory ──────────────────────────────────────────────────────────────


def add_rate_limiting(app: FastAPI) -> None:
    """
    Add rate limiting middleware to a FastAPI app.
    Call during app initialization.
    """
    app.add_middleware(RateLimitMiddleware)
    logger.info("Rate limiting enabled (default=%d/min, auth=%d/min, ai=%d/min)",
                 RATE_LIMIT_DEFAULT, RATE_LIMIT_AUTH, RATE_LIMIT_AI)
