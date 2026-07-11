from __future__ import annotations


class RecommendationEngine:
    """
    Generates actionable recommendations
    based on job matching results.
    """

    @staticmethod
    def generate(
        missing_skills: list[str],
        overall_score: float,
    ) -> list[str]:

        recommendations: list[str] = []

        # ==================================================
        # Skill Recommendations
        # ==================================================

        for skill in missing_skills:
            recommendations.append(
                f"Learn {skill}"
            )

            recommendations.append(
                f"Add a hands-on project using {skill}"
            )

        # ==================================================
        # Resume Recommendations
        # ==================================================

        if missing_skills:
            recommendations.append(
                "Update your resume after learning the missing skills."
            )

        # ==================================================
        # Match Recommendation
        # ==================================================

        if overall_score >= 90:

            recommendations.append(
                "Excellent match. Apply immediately."
            )

        elif overall_score >= 80:

            recommendations.append(
                "Strong match. Apply after tailoring your resume."
            )

        elif overall_score >= 65:

            recommendations.append(
                "Improve the missing skills before applying."
            )

            recommendations.append(
                "Customize your resume for this job description."
            )

        else:

            recommendations.append(
                "Gain more relevant experience before applying."
            )

            recommendations.append(
                "Build two or three portfolio projects related to this role."
            )

        # ==================================================
        # Remove duplicates
        # ==================================================

        return list(dict.fromkeys(recommendations))