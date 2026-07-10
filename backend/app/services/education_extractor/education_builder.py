from __future__ import annotations

from backend.app.services.education_extractor.degree_detector import (
    detect_degrees,
)
from backend.app.services.education_extractor.education_models import (
    EducationRecord,
)
from backend.app.services.education_extractor.specialization_detector import (
    detect_specializations,
)


def build_education(
    block: str,
) -> EducationRecord:
    """
    Build a canonical EducationRecord from
    one education block.

    Current Version
    ---------------
    ✓ Degree
    ✓ Specialization

    Upcoming
    --------
    - Institution
    - University
    - Location
    - Dates
    - Grade / CGPA
    - Confidence
    """

    degrees = detect_degrees(block)

    specializations = detect_specializations(block)

    return EducationRecord(
        degree=(
            degrees[0]
            if degrees
            else None
        ),
        specialization=(
            specializations[0]
            if specializations
            else None
        ),
    )