from backend.app.services.job_matching.models import MatchComponent


class EducationMatcher:
    """
    Deterministic education matching.
    """

    DEGREE_RANK = {
        "": 0,
        "Diploma": 1,
        "Bachelor": 2,
        "Master": 3,
        "PhD": 4,
    }

    @classmethod
    def match(
        cls,
        candidate_degree: str,
        required_degree: str,
    ) -> MatchComponent:

        candidate_rank = cls.DEGREE_RANK.get(candidate_degree, 0)
        required_rank = cls.DEGREE_RANK.get(required_degree, 0)

        if candidate_rank == 0:
            score = 0.0
        elif candidate_rank >= required_rank:
            score = 100.0
        else:
            score = 50.0

        return MatchComponent(
            score=score,
            matched=[],
            missing=[],
            reasons=[],
        )