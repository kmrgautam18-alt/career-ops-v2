from __future__ import annotations

from pathlib import Path
import re


RESOURCE_FILE = (
    Path(__file__).parent.parent.parent
    / "resources"
    / "designations"
    / "common_designations.txt"
)


class DesignationDetector:
    """
    Rule-based designation detector.

    Current Version
    ---------------
    - Knowledge base matching
    - Regex word-boundary matching
    - Duplicate removal

    Future Versions
    ---------------
    - AI Extraction
    - LLM
    - Embedding Search
    """

    def __init__(self) -> None:
        self.designations = self._load_designations()

    def _load_designations(self) -> list[str]:

        if not RESOURCE_FILE.exists():
            return []

        titles = []

        with open(
            RESOURCE_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            for line in file:

                value = line.strip()

                if value:
                    titles.append(value)

        # Longest first
        titles.sort(
            key=len,
            reverse=True,
        )

        return titles

    def detect(
        self,
        text: str,
    ) -> list[str]:

        if not text:
            return []

        normalized = text.lower()

        found = set()

        for designation in self.designations:

            pattern = (
                r"\b"
                + re.escape(designation.lower())
                + r"\b"
            )

            if re.search(pattern, normalized):
                found.add(designation)

        return sorted(
    found,
    key=len,
    reverse=True,
)


_detector = DesignationDetector()


def detect_designations(
    text: str,
) -> list[str]:
    """
    Stable public API.

    Future implementations may switch to
    AI while preserving this interface.
    """

    return _detector.detect(text)