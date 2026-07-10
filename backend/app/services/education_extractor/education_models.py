from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class EducationRecord:
    """
    Canonical education object.

    Every education extractor
    must return this structure.

    Future
    -------
    AI Extractor
    OCR Extractor
    Hybrid Extractor
    """

    degree: str | None = None

    specialization: str | None = None

    institution: str | None = None

    location: str | None = None

    university: str | None = None

    start_date: date | None = None

    end_date: date | None = None

    grade: str | None = None

    percentage: float | None = None

    cgpa: float | None = None

    currently_studying: bool = False

    description: str | None = None

    confidence: float = 1.0

    source: str = "knowledge_base"