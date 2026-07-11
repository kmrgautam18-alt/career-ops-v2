from __future__ import annotations

from backend.app.services.ai.resume_optimizer.models import (
    OptimizationSuggestion,
)


class ResumeRecommendationEngine:
    """
    Generates resume optimization suggestions.
    """

    @staticmethod
    def generate(
        missing_keywords: list[str],
    ) -> list[OptimizationSuggestion]:

        suggestions: list[OptimizationSuggestion] = []

        for keyword in missing_keywords:

            suggestions.append(
                OptimizationSuggestion(
                    title=f"Add keyword: {keyword}",
                    current="Keyword missing",
                    suggested=(
                        f"Include {keyword} naturally inside your "
                        "experience, projects or skills."
                    ),
                    priority="HIGH",
                )
            )

        if missing_keywords:

            suggestions.append(
                OptimizationSuggestion(
                    title="Improve ATS Match",
                    current="Resume lacks important skills",
                    suggested=(
                        "Update your resume after gaining "
                        "the missing skills."
                    ),
                    priority="MEDIUM",
                )
            )

        return suggestions