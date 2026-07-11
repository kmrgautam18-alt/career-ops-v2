from __future__ import annotations

from backend.app.services.ai.ats.ats_models import ATSRecommendation


class RecommendationBuilder:
    """
    Builds ATS improvement recommendations.
    """

    @staticmethod
    def build(
        missing_keywords: list[str],
        missing_sections: list[str],
        formatting_recommendations: list[str],
    ) -> list[ATSRecommendation]:

        recommendations: list[ATSRecommendation] = []

        # Missing Skills
        for keyword in missing_keywords:
            recommendations.append(
                ATSRecommendation(
                    title=f"Add keyword: {keyword}",
                    description=(
                        f"Include '{keyword}' naturally in your resume."
                    ),
                    priority="HIGH",
                )
            )

        # Missing Sections
        for section in missing_sections:
            recommendations.append(
                ATSRecommendation(
                    title=f"Add {section} section",
                    description=(
                        f"Your resume is missing the {section} section."
                    ),
                    priority="HIGH",
                )
            )

        # Formatting
        for recommendation in formatting_recommendations:
            recommendations.append(
                ATSRecommendation(
                    title="Formatting Improvement",
                    description=recommendation,
                    priority="MEDIUM",
                )
            )

        return recommendations