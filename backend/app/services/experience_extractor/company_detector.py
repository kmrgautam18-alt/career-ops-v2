from __future__ import annotations

import re
from pathlib import Path

RESOURCE_DIR = (
    Path(__file__).parent.parent.parent
    / "resources"
    / "companies"
)


class CompanyDetector:
    """
    Detect company names from resume text.

    Detection Strategy
    ------------------
    1. Known company lookup
    2. Company suffix matching
    3. AI detector (future)
    """

    def __init__(self):

        self.known_companies = self._load_file(
            "known_companies.txt",
        )

        self.company_suffixes = self._load_file(
            "common_suffixes.txt",
        )

    def _load_file(
        self,
        filename: str,
    ) -> set[str]:

        path = RESOURCE_DIR / filename

        values: set[str] = set()

        if not path.exists():
            return values

        with open(
            path,
            encoding="utf-8",
        ) as f:

            for line in f:

                value = line.strip()

                if value:
                    values.add(value)

        return values

    def detect(
        self,
        text: str,
    ) -> list[str]:

        if not text:
            return []

        found = set()

        normalized = text.lower()

        # ------------------------------------
        # Layer 1
        # Known Companies
        # ------------------------------------

        for company in self.known_companies:

            pattern = (
                r"\b"
                + re.escape(company.lower())
                + r"\b"
            )

            if re.search(
                pattern,
                normalized,
            ):
                found.add(company)

        # ------------------------------------
        # Future:
        #
        # Layer 2
        # Suffix Heuristics
        #
        # Layer 3
        # AI Extraction
        # ------------------------------------

        return sorted(found)


_default_detector = CompanyDetector()


def detect_companies(
    text: str,
) -> list[str]:

    return _default_detector.detect(text)