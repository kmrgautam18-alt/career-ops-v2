class RecommendationEngine:
    """
    Generates deterministic recommendations from match results.
    """

    @staticmethod
    def generate(
        missing_skills: list[str],
        overall_score: float,
    ) -> list[str]:

        recommendations = []

        for skill in missing_skills:
            recommendations.append(f"Learn {skill}")

        if overall_score >= 90:
            recommendations.append(
                "Excellent match. Apply immediately."
            )
        elif overall_score >= 80:
            recommendations.append(
                "Strong match. Consider applying."
            )
        elif overall_score >= 65:
            recommendations.append(
                "Improve missing skills before applying."
            )
        else:
            recommendations.append(
                "Strengthen your resume before applying."
            )

        return recommendations