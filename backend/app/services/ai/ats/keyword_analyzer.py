from __future__ import annotations


class KeywordAnalyzer:
    """
    Analyzes how many required keywords
    are present inside the resume.
    """

    @staticmethod
    def analyze(
        resume_text: str,
        keywords: list[str],
    ) -> tuple[float, list[str]]:
        """
        Returns:
            score (0-100)
            missing keywords
        """

        if not keywords:
            return 100.0, []

        text = resume_text.lower()

        matched = []
        missing = []

        for keyword in keywords:
            if keyword.lower() in text:
                matched.append(keyword)
            else:
                missing.append(keyword)

        score = (len(matched) / len(keywords)) * 100

        return round(score, 2), missing