from __future__ import annotations

from backend.app.services.ai.ats.constants import (
    FORMATTING_WEIGHT,
    KEYWORD_WEIGHT,
    READABILITY_WEIGHT,
    SECTION_WEIGHT,
)


class ATSScoreCalculator:
    """
    Calculates the weighted ATS score.
    """

    @staticmethod
    def calculate(
        keyword_score: float,
        formatting_score: float,
        section_score: float,
        readability_score: float = 100.0,
    ) -> float:
        """
        Returns a weighted ATS score (0-100).
        """

        score = (
            (keyword_score * KEYWORD_WEIGHT)
            + (formatting_score * FORMATTING_WEIGHT)
            + (section_score * SECTION_WEIGHT)
            + (readability_score * READABILITY_WEIGHT)
        ) / 100

        return round(score, 2)