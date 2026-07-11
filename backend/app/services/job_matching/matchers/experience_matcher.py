from backend.app.services.job_matching.models import MatchComponent


class ExperienceMatcher:
    @staticmethod
    def match(
        candidate_years: float,
        required_years: float,
    ) -> MatchComponent:

        if required_years <= 0:
            score = 100.0
        elif candidate_years >= required_years:
            score = 100.0
        else:
            score = round(
                (candidate_years / required_years) * 100,
                2,
            )

        return MatchComponent(
            score=score,
            matched=[],
            missing=[],
            reasons=[],
        )