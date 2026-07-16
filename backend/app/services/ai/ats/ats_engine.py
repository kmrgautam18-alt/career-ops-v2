"""ATS evaluation engine powered by Gemini AI."""

from __future__ import annotations

import logging
from typing import Any

from backend.app.services.ai.ats.ats_models import (
    ATSReport,
    ATSScoreBreakdown,
)
from backend.app.services.ai.ats.recommendation_builder import (
    RecommendationBuilder,
)
from backend.app.services.llm_service import (
    LLMServiceError,
    ats_evaluate,
)

logger = logging.getLogger(__name__)


class ATSEngine:
    """Main ATS evaluation engine using AI-powered analysis."""

    @staticmethod
    def evaluate(
        resume_text: str,
        required_keywords: list[str],
        job_description: str = "",
    ) -> ATSReport:
        # Use job description if provided, otherwise use keywords as description
        desc = job_description or "Required keywords: " + ", ".join(required_keywords)

        try:
            result = ats_evaluate(resume_text, desc)
            return ATSEngine._parse_result(result)
        except LLMServiceError as e:
            logger.warning(f"LLM ATS evaluation failed, using fallback: {e}")
            return ATSEngine._fallback_evaluate(resume_text, required_keywords)

    @staticmethod
    def _parse_result(result: dict[str, Any]) -> ATSReport:
        score = ATSScoreBreakdown(
            keywords=result.get("keyword_score", 50),
            formatting=result.get("formatting_score", 50),
            sections=result.get("section_score", 50),
            readability=result.get("readability_score", 50),
            overall=result.get("overall_score", 50),
        )

        recs_data = result.get("recommendations", [])
        recommendations = []
        for r in recs_data:
            if isinstance(r, dict):
                recommendations.append(
                    {
                        "title": r.get("title", "Suggestion"),
                        "description": r.get("description", ""),
                        "priority": r.get("priority", "medium"),
                    }
                )

        return ATSReport(
            score=score,
            recommendations=recommendations or RecommendationBuilder.build([], [], []),
            strengths=result.get("strengths", []),
            weaknesses=result.get("weaknesses", []),
        )

    @staticmethod
    def _fallback_evaluate(
        resume_text: str,
        required_keywords: list[str],
    ) -> ATSReport:
        """Rule-based fallback when LLM is unavailable."""
        from backend.app.services.ai.ats.ats_score_calculator import (
            ATSScoreCalculator,
        )
        from backend.app.services.ai.ats.formatting_analyzer import (
            FormattingAnalyzer,
        )
        from backend.app.services.ai.ats.keyword_analyzer import (
            KeywordAnalyzer,
        )
        from backend.app.services.ai.ats.section_analyzer import (
            SectionAnalyzer,
        )

        keyword_score, missing_keywords = KeywordAnalyzer.analyze(
            resume_text, required_keywords
        )
        formatting_score, formatting_recs = FormattingAnalyzer.analyze(resume_text)
        section_score, missing_sections = SectionAnalyzer.analyze(resume_text)
        readability_score = 100.0

        overall = ATSScoreCalculator.calculate(
            keyword_score, formatting_score, section_score, readability_score
        )

        recommendations = RecommendationBuilder.build(
            missing_keywords, missing_sections, formatting_recs
        )

        return ATSReport(
            score=ATSScoreBreakdown(
                keywords=keyword_score,
                formatting=formatting_score,
                sections=section_score,
                readability=readability_score,
                overall=overall,
            ),
            recommendations=recommendations,
            strengths=[],
            weaknesses=[],
        )
