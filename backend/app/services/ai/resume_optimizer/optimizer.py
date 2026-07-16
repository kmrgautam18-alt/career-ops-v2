"""Resume optimization engine powered by Gemini AI."""

from __future__ import annotations

import logging
from typing import Any

from backend.app.services.llm_service import (
    optimize_resume,
    LLMServiceError,
)
from backend.app.services.ai.resume_optimizer.models import (
    OptimizationReport,
)

logger = logging.getLogger(__name__)


class ResumeOptimizer:
    """Resume optimization engine using AI-powered analysis."""

    @staticmethod
    def optimize(
        resume_text: str,
        required_keywords: list[str],
        job_description: str = "",
    ) -> OptimizationReport:
        desc = job_description or "Required keywords: " + ", ".join(required_keywords)

        try:
            result = optimize_resume(resume_text, desc)
            return ResumeOptimizer._parse_result(result, resume_text, required_keywords)
        except LLMServiceError as e:
            logger.warning(f"LLM resume optimization failed, using fallback: {e}")
            return ResumeOptimizer._fallback(resume_text, required_keywords)

    @staticmethod
    def _parse_result(
        result: dict[str, Any],
        resume_text: str,
        required_keywords: list[str],
    ) -> OptimizationReport:
        from backend.app.services.ai.resume_optimizer.models import (
            OptimizationSuggestion,
        )

        missing_keywords = result.get("missing_keywords", [])
        suggestions_data = result.get("suggestions", [])
        suggestions = []

        for s in suggestions_data:
            if isinstance(s, dict):
                suggestions.append(
                    OptimizationSuggestion(
                        title=s.get("title", "Improvement"),
                        current=s.get("current", ""),
                        suggested=s.get("suggested", ""),
                        priority=s.get("priority", "medium"),
                    )
                )

        return OptimizationReport(
            ats_score_before=result.get("ats_score_before", 50),
            ats_score_after=result.get("ats_score_after", 70),
            missing_keywords=missing_keywords,
            suggestions=suggestions,
        )

    @staticmethod
    def _fallback(
        resume_text: str,
        required_keywords: list[str],
    ) -> OptimizationReport:
        """Rule-based fallback when LLM is unavailable."""
        from backend.app.services.ai.ats.ats_engine import ATSEngine
        from backend.app.services.ai.resume_optimizer.recommendation_engine import (
            ResumeRecommendationEngine,
        )

        ats_report = ATSEngine.evaluate(
            resume_text=resume_text,
            required_keywords=required_keywords,
        )

        missing_keywords = [
            r.title.replace("Add keyword: ", "")
            for r in ats_report.recommendations
            if r.title.startswith("Add keyword:")
        ]

        suggestions = ResumeRecommendationEngine.generate(missing_keywords)

        return OptimizationReport(
            ats_score_before=ats_report.score.overall,
            ats_score_after=min(ats_report.score.overall + 20, 100),
            missing_keywords=missing_keywords,
            suggestions=suggestions,
        )
