from __future__ import annotations

from backend.app.services.ai.ats.ats_models import (
    ATSReport,
    ATSScoreBreakdown,
)
from backend.app.services.ai.ats.ats_score_calculator import (
    ATSScoreCalculator,
)
from backend.app.services.ai.ats.formatting_analyzer import (
    FormattingAnalyzer,
)
from backend.app.services.ai.ats.keyword_analyzer import (
    KeywordAnalyzer,
)
from backend.app.services.ai.ats.recommendation_builder import (
    RecommendationBuilder,
)
from backend.app.services.ai.ats.section_analyzer import (
    SectionAnalyzer,
)


class ATSEngine:
    """
    Main ATS evaluation engine.
    """

    @staticmethod
    def evaluate(
        resume_text: str,
        required_keywords: list[str],
    ) -> ATSReport:

        keyword_score, missing_keywords = (
            KeywordAnalyzer.analyze(
                resume_text,
                required_keywords,
            )
        )

        formatting_score, formatting_recommendations = (
            FormattingAnalyzer.analyze(
                resume_text,
            )
        )

        section_score, missing_sections = (
            SectionAnalyzer.analyze(
                resume_text,
            )
        )

        readability_score = 100.0

        overall = ATSScoreCalculator.calculate(
            keyword_score,
            formatting_score,
            section_score,
            readability_score,
        )

        recommendations = RecommendationBuilder.build(
            missing_keywords,
            missing_sections,
            formatting_recommendations,
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
        )