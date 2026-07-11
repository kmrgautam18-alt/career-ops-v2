from __future__ import annotations

from dataclasses import dataclass, field

from backend.app.services.education_extractor.education_models import (
    EducationRecord,
)
from backend.app.services.experience_extractor.experience_models import (
    ExperienceRecord,
)


@dataclass(slots=True)
class ResumeInformation:
    """
    Canonical structured resume information.

    Every extractor contributes to this model.
    """

    experiences: list[ExperienceRecord] = field(
        default_factory=list,
    )

    education: list[EducationRecord] = field(
        default_factory=list,
    )

    skills: list[str] = field(
        default_factory=list,
    )

    certifications: list = field(
        default_factory=list,
    )

    projects: list = field(
        default_factory=list,
    )