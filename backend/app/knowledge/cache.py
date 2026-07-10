from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar


T = TypeVar("T")


class KnowledgeCache:
    """
    Simple in-memory cache.

    Current
    -------
    - Process memory cache

    Future
    -------
    - Redis
    - TTL
    - Cache invalidation
    """

    def __init__(self) -> None:

        self._cache: dict[str, object] = {}

    def get_or_load(
        self,
        key: str,
        loader: Callable[[], T],
    ) -> T:

        if key not in self._cache:

            self._cache[key] = loader()

        return self._cache[key]  # type: ignore[return-value]

    def clear(self) -> None:

        self._cache.clear()


knowledge_cache = KnowledgeCache()