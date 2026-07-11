from backend.app.services.job_matching.models import MatchComponent


class LocationMatcher:
    @staticmethod
    def match(
        candidate: str,
        job: str,
        remote: bool = False,
    ) -> MatchComponent:

        if remote:
            score = 100.0
        elif candidate.strip().lower() == job.strip().lower():
            score = 100.0
        else:
            score = 50.0

        return MatchComponent(
            score=score,
            matched=[],
            missing=[],
            reasons=[],
        )