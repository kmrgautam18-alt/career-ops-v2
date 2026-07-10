from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class ExperienceRecord:
    """
    Canonical experience object.

    Every experience extractor
    (Regex, AI, Hybrid, LLM)
    MUST return this structure.
    """

    company: str | None = None

    designation: str | None = None

    employment_type: str | None = None

    location: str | None = None

    start_date: date | None = None

    end_date: date | None = None

    currently_working: bool = False

    duration_months: int | None = None

    description: str | None = None

    confidence: float = 1.0

    source: str = "knowledge_base"