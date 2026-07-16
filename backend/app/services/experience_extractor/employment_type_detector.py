from __future__ import annotations

from enum import Enum

from backend.app.services.experience_extractor.utils import (
    normalize_text,
)


class EmploymentType(str, Enum):  # noqa: UP042
    FULL_TIME = "Full Time"
    PART_TIME = "Part Time"
    INTERNSHIP = "Internship"
    CONTRACT = "Contract"
    FREELANCE = "Freelance"
    CONSULTANT = "Consultant"
    TEMPORARY = "Temporary"
    UNKNOWN = "Unknown"


EMPLOYMENT_KEYWORDS = {
    EmploymentType.FULL_TIME: [
        "full time",
        "full-time",
    ],
    EmploymentType.PART_TIME: [
        "part time",
        "part-time",
    ],
    EmploymentType.INTERNSHIP: [
        "intern",
        "internship",
    ],
    EmploymentType.CONTRACT: [
        "contract",
        "contractor",
    ],
    EmploymentType.FREELANCE: [
        "freelance",
        "freelancer",
    ],
    EmploymentType.CONSULTANT: [
        "consultant",
        "consulting",
    ],
    EmploymentType.TEMPORARY: [
        "temporary",
        "temp",
    ],
}


def detect_employment_type(
    text: str,
) -> EmploymentType:
    """
    Detect employment type using rule-based matching.

    Future versions can replace this implementation
    with AI/LLM while preserving the same interface.
    """

    normalized = normalize_text(text)

    for employment_type, keywords in EMPLOYMENT_KEYWORDS.items():

        for keyword in keywords:

            if keyword in normalized:
                return employment_type

    return EmploymentType.UNKNOWN