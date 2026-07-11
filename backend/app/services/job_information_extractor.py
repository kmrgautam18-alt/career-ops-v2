from __future__ import annotations

import re
from dataclasses import dataclass, field

from backend.app.services.education_extractor.extractor import (
    extract_education,
)
from backend.app.services.skill_extractor.skill_detector import (
    detect_skills,
)


@dataclass(slots=True)
class JobInformation:
    """
    Structured information extracted from a job description.
    """

    skills: list[str] = field(default_factory=list)

    required_years: float = 0.0

    required_degree: str = ""

    certifications: list[str] = field(default_factory=list)

    location: str = ""

    remote: bool = False

    text: str = ""


def _extract_required_years(
    text: str,
) -> float:
    """
    Extract required years of experience.

    Examples

    3 years

    5+ years

    8 yrs

    10 years experience
    """

    patterns = [
        r"(\d+)\+?\s*(?:years|year|yrs|yr)",
        r"experience.{0,15}?(\d+)\+?",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:

            return float(match.group(1))

    return 0.0


def _extract_degree(
    text: str,
) -> str:
    """
    Extract the highest detected degree.
    """

    education = extract_education(text)

    if education:

        return education[0].degree or ""

    return ""


def _detect_remote(
    text: str,
) -> bool:

    return "remote" in text.lower()


def extract_job_information(
    description: str | None,
) -> JobInformation:
    """
    Extract structured information
    from a job description.
    """

    description = description or ""

    return JobInformation(
        skills=detect_skills(description),
        required_years=_extract_required_years(
            description,
        ),
        required_degree=_extract_degree(
            description,
        ),
        certifications=[],
        location="",
        remote=_detect_remote(
            description,
        ),
        text=description,
    )