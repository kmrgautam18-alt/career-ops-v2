"""
Redis Caching Service for Career-Ops.
Provides cache decorators and helpers for:
- Dashboard stats (5 min TTL)
- Job listings (2 min TTL)
- AI results (10 min TTL)
- User profiles (15 min TTL)
"""

from __future__ import annotations

import functools
import hashlib
import json
import logging
import time
from typing import Any, Callable

from backend.app.core.config import settings

logger = logging.getLogger(__name__)

# Attempt Redis import — gracefully degrade if not available
try:
    import redis.asyncio as aioredis
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("redis package not installed — caching disabled")


class CacheService:
    """Redis-backed cache service with TTL support and graceful fallback."""

    def __init__(self) -> None:
        self._client: redis.Redis | aioredis.Redis | None = None
        self._enabled = settings.REDIS_ENABLED and REDIS_AVAILABLE
        self._prefix = "careerops:"

    def _connect(self) -> redis.Redis | None:
        """Lazy Redis connection."""
        if not self._enabled:
            return None
        if self._client is not None:
            return self._client
        try:
            self._client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD or None,
                db=settings.REDIS_DB,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=3,
                retry_on_timeout=False,
            )
            self._client.ping()
            logger.info("Connected to Redis at %s:%d", settings.REDIS_HOST, settings.REDIS_PORT)
            return self._client
        except Exception as e:
            logger.warning("Redis connection failed — caching disabled: %s", e)
            self._enabled = False
            return None

    def _key(self, *parts: str) -> str:
        """Build a namespaced cache key."""
        return f"{self._prefix}{':'.join(parts)}"

    def get(self, *key_parts: str) -> Any | None:
        """Retrieve a value from cache."""
        client = self._connect()
        if not client:
            return None
        try:
            data = client.get(self._key(*key_parts))
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.debug("Cache GET error: %s", e)
            return None

    def set(self, ttl: int, *key_parts: str, value: Any) -> bool:
        """Store a value in cache with TTL (seconds)."""
        client = self._connect()
        if not client:
            return False
        try:
            client.setex(self._key(*key_parts), ttl, json.dumps(value, default=str))
            return True
        except Exception as e:
            logger.debug("Cache SET error: %s", e)
            return False

    def delete(self, *key_parts: str) -> bool:
        """Delete a cache key."""
        client = self._connect()
        if not client:
            return False
        try:
            client.delete(self._key(*key_parts))
            return True
        except Exception as e:
            logger.debug("Cache DELETE error: %s", e)
            return False

    def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching a pattern (e.g., 'dashboard:*')."""
        client = self._connect()
        if not client:
            return 0
        try:
            cursor = 0
            deleted = 0
            while True:
                cursor, keys = client.scan(cursor, match=self._key(pattern), count=100)
                if keys:
                    deleted += client.delete(*keys)
                if cursor == 0:
                    break
            return deleted
        except Exception as e:
            logger.debug("Cache DELETE pattern error: %s", e)
            return 0

    def flush_namespace(self, namespace: str) -> int:
        """Flush all keys in a namespace (e.g., 'jobs', 'dashboard')."""
        return self.delete_pattern(f"{namespace}:*")


# Global cache service instance
cache = CacheService()


# ── Decorators ──────────────────────────────────────────────────────────


def cached(ttl: int, namespace: str = "default"):
    """
    Decorator that caches the return value of a function.

    Usage:
        @cached(ttl=300, namespace="dashboard")
        def get_dashboard_stats(user_id: int):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Build a cache key from args/kwargs
            key_parts = [namespace, func.__name__]
            if args:
                key_parts.append(hashlib.md5(str(args).encode()).hexdigest()[:12])
            if kwargs:
                key_parts.append(hashlib.md5(str(sorted(kwargs.items())).encode()).hexdigest()[:12])

            # Try cache first
            result = cache.get(*key_parts)
            if result is not None:
                return result

            # Execute and cache
            result = func(*args, **kwargs)
            cache.set(ttl, *key_parts, value=result)
            return result
        return wrapper
    return decorator


def invalidate_cache(namespace: str):
    """
    Decorator that invalidates a cache namespace after function execution.
    Use on create/update/delete functions.

    Usage:
        @invalidate_cache("dashboard")
        def create_application(...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            cache.flush_namespace(namespace)
            return result
        return wrapper
    return decorator
