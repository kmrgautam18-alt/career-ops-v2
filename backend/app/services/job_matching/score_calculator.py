"""
Weighted score calculator for the Job Matching Engine.
"""

from .config import (
    CERTIFICATION_WEIGHT,
    EDUCATION_WEIGHT,
    EXPERIENCE_WEIGHT,
    KEYWORD_WEIGHT,
    LOCATION_WEIGHT,
    SKILL_WEIGHT,
)


class ScoreCalculator:
    """
    Calculates the final weighted score.
    """

    @staticmethod
    def calculate(
        *,
        skill: float,
        experience: float,
        education: float,
        certification: float,
        keyword: float,
        location: float,
    ) -> float:
        score = (
            skill * SKILL_WEIGHT
            + experience * EXPERIENCE_WEIGHT
            + education * EDUCATION_WEIGHT
            + certification * CERTIFICATION_WEIGHT
            + keyword * KEYWORD_WEIGHT
            + location * LOCATION_WEIGHT
        )

        return round(score, 2)