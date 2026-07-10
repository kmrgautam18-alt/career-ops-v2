from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SkillRecord:
    """
    Canonical skill object.

    Every skill extractor
    must return this structure.

    Future
    -------
    AI Extractor
    Hybrid Extractor
    OCR Extractor
    """

    name: str

    category: str | None = None

    years_of_experience: float | None = None

    confidence: float = 1.0

    source: str = "knowledge_base"