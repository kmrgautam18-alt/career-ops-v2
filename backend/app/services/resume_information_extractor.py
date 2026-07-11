from __future__ import annotations

from backend.app.services.education_extractor.extractor import (
    extract_education,
)
from backend.app.services.experience_extractor.extractor import (
    extract_experiences,
)
from backend.app.services.resume_information_models import (
    ResumeInformation,
)
from backend.app.services.skill_extractor.skill_detector import (
    detect_skills,
)


def extract_resume_information(
    resume_text: str,
) -> ResumeInformation:
    """
    Extract structured information from a resume.

    Current Features
    ----------------
    ✓ Experience
    ✓ Education
    ✓ Skills

    Future
    ------
    - Certifications
    - Projects
    """

    information = ResumeInformation()

    # =====================================================
    # Experience
    # =====================================================

    information.experiences = extract_experiences(
        resume_text,
    )

    # =====================================================
    # Education
    # =====================================================

    information.education = extract_education(
        resume_text,
    )

    # =====================================================
    # Skills
    # =====================================================

    information.skills = detect_skills(
        resume_text,
    )

    # =====================================================
    # Future Modules
    # =====================================================

    information.certifications = []

    information.projects = []

    return information


# ==========================================================
# Backward Compatibility
# ==========================================================


def extract_profile(
    resume_text: str,
) -> ResumeInformation:
    """
    Backward-compatible wrapper.
    """

    return extract_resume_information(
        resume_text,
    )