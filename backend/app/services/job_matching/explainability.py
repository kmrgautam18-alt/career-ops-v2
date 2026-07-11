class ExplainabilityEngine:
    """
    Generates human-readable explanations for match results.
    """

    @staticmethod
    def generate(
        matched_skills: list[str],
        missing_skills: list[str],
    ) -> list[str]:

        explanations = []

        for skill in matched_skills:
            explanations.append(
                f"Matched skill: {skill}"
            )

        for skill in missing_skills:
            explanations.append(
                f"Missing skill: {skill}"
            )

        return explanations