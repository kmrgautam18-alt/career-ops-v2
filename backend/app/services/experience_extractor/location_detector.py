from __future__ import annotations

import re

from backend.app.knowledge.engine import (
    knowledge_engine,
)


class LocationDetector:
    """
    Rule-based location detector.

    Current
    -------
    - Knowledge base lookup
    - Word boundary matching
    - Duplicate removal

    Future
    ------
    - Database knowledge
    - AI extraction
    - Geo normalization
    """

    def __init__(self) -> None:

        self.locations = sorted(
            knowledge_engine.locations(),
            key=len,
            reverse=True,
        )

    def detect(
        self,
        text: str,
    ) -> list[str]:

        if not text:
            return []

        normalized = text.lower()

        found: set[str] = set()

        for location in self.locations:

            pattern = (
                r"\b"
                + re.escape(location.lower())
                + r"\b"
            )

            if re.search(
                pattern,
                normalized,
            ):
                found.add(location)

        return sorted(
            found,
            key=len,
            reverse=True,
        )


_detector = LocationDetector()


def detect_locations(
    text: str,
) -> list[str]:
    """
    Stable public API.
    """

    return _detector.detect(text)