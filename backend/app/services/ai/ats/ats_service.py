from __future__ import annotations

from backend.app.services.ai.ats.ats_engine import ATSEngine


class ATSService:
    """
    Service layer for ATS evaluation.
    """

    @staticmethod
    def evaluate_resume(
        resume_text: str,
        required_keywords: list[str],
    ):
        return ATSEngine.evaluate(
            resume_text=resume_text,
            required_keywords=required_keywords,
        )