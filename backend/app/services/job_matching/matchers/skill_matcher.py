"""
Skill Matcher for Job Matching Engine.
"""

from backend.app.services.job_matching.models import MatchComponent


class SkillMatcher:
    """
    Compares candidate skills against required job skills.
    """

    @staticmethod
    def match(
        candidate_skills: list[str],
        required_skills: list[str],
    ) -> MatchComponent:

        candidate = {s.strip().lower() for s in candidate_skills}
        required = {s.strip().lower() for s in required_skills}

        matched = sorted(candidate & required)
        missing = sorted(required - candidate)

        if not required:
            score = 100.0
        else:
            score = round((len(matched) / len(required)) * 100, 2)

        reasons = [
            f"Matched {len(matched)} of {len(required)} required skills."
        ]

        return MatchComponent(
            score=score,
            matched=matched,
            missing=missing,
            reasons=reasons,
        )