from __future__ import annotations

from backend.app.services.ai.ats.constants import REQUIRED_SECTIONS


class SectionAnalyzer:
    """
    Checks whether important ATS resume
    sections are present.
    """

    @staticmethod
    def analyze(
        resume_text: str,
    ) -> tuple[float, list[str]]:
        """
        Returns:
            score (0-100)
            missing sections
        """

        text = resume_text.lower()

        found = 0
        missing: list[str] = []

        for section in REQUIRED_SECTIONS:
            if section in text:
                found += 1
            else:
                missing.append(section.title())

        score = (found / len(REQUIRED_SECTIONS)) * 100

        return round(score, 2), missing