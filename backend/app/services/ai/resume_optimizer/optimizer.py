from __future__ import annotations

from backend.app.services.ai.ats.ats_engine import ATSEngine
from backend.app.services.ai.resume_optimizer.models import (
    OptimizationReport,
)
from backend.app.services.ai.resume_optimizer.recommendation_engine import (
    ResumeRecommendationEngine,
)


class ResumeOptimizer:
    """
    Resume optimization engine.
    """

    @staticmethod
    def optimize(
        resume_text: str,
        required_keywords: list[str],
    ) -> OptimizationReport:

        ats_report = ATSEngine.evaluate(
            resume_text=resume_text,
            required_keywords=required_keywords,
        )

        missing_keywords = [
            recommendation.title.replace(
                "Add keyword: ",
                "",
            )
            for recommendation in ats_report.recommendations
            if recommendation.title.startswith("Add keyword:")
        ]

        suggestions = ResumeRecommendationEngine.generate(
            missing_keywords,
        )

        return OptimizationReport(
            ats_score_before=ats_report.score.overall,
            ats_score_after=min(
                ats_report.score.overall + 20,
                100,
            ),
            missing_keywords=missing_keywords,
            suggestions=suggestions,
        )