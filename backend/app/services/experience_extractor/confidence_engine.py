from __future__ import annotations

from backend.app.services.experience_extractor.experience_models import (
    ExperienceRecord,
)

CONFIDENCE_WEIGHTS = {
    "company": 0.20,
    "designation": 0.20,
    "dates": 0.20,
    "employment_type": 0.10,
    "location": 0.10,
    "description": 0.10,
    "duration": 0.10,
}


def calculate_confidence(
    record: ExperienceRecord,
) -> float:
    """
    Calculate extraction confidence.

    Current Version
    ---------------
    Rule-based scoring.

    Future
    ---------------
    AI confidence
    ML confidence
    """

    score = 0.0

    if record.company:
        score += CONFIDENCE_WEIGHTS["company"]

    if record.designation:
        score += CONFIDENCE_WEIGHTS["designation"]

    if record.start_date:
        score += CONFIDENCE_WEIGHTS["dates"]

    if record.employment_type:
        score += CONFIDENCE_WEIGHTS["employment_type"]

    if record.location:
        score += CONFIDENCE_WEIGHTS["location"]

    if record.description:
        score += CONFIDENCE_WEIGHTS["description"]

    if record.duration_months is not None:
        score += CONFIDENCE_WEIGHTS["duration"]

    return round(
        min(score, 1.0),
        2,
    )