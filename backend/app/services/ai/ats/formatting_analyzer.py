from __future__ import annotations


class FormattingAnalyzer:
    """
    Performs lightweight formatting checks
    for ATS compatibility.
    """

    @staticmethod
    def analyze(
        resume_text: str,
    ) -> tuple[float, list[str]]:
        """
        Returns:
            score (0-100)
            recommendations
        """

        score = 100.0
        recommendations: list[str] = []

        if len(resume_text.splitlines()) < 10:
            score -= 20
            recommendations.append(
                "Resume appears too short."
            )

        if "•" not in resume_text and "-" not in resume_text:
            score -= 20
            recommendations.append(
                "Use bullet points for achievements."
            )

        if len(resume_text) < 300:
            score -= 20
            recommendations.append(
                "Add more professional details."
            )

        score = max(score, 0)

        return score, recommendations