from __future__ import annotations

from backend.app.services.experience_extractor.extractor import (
    extract_experiences,
)
from backend.app.services.resume_information_models import (
    ResumeInformation,
)


def extract_resume_information(
    resume_text: str,
) -> ResumeInformation:
    """
    Extract structured information
    from a resume.

    Current Version
    ---------------
    ✓ Experience

    Upcoming
    --------
    - Education
    - Skills
    - Projects
    - Certifications
    """

    information = ResumeInformation()

    information.experiences = extract_experiences(
        resume_text,
    )

    return information


# ==========================================================
# Backward Compatibility
# ==========================================================

def extract_profile(
    resume_text: str,
) -> ResumeInformation:
    """
    Temporary compatibility wrapper.

    Existing services still call
    extract_profile().

    TODO:
    Remove after Resume Upload Service
    is migrated.
    """

    return extract_resume_information(
        resume_text,
    )