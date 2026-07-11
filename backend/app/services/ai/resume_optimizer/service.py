from __future__ import annotations

from backend.app.services.ai.resume_optimizer.optimizer import (
    ResumeOptimizer,
)


class ResumeOptimizerService:
    """
    Service layer for resume optimization.
    """

    @staticmethod
    def optimize_resume(
        resume_text: str,
        required_keywords: list[str],
    ):
        return ResumeOptimizer.optimize(
            resume_text=resume_text,
            required_keywords=required_keywords,
        )