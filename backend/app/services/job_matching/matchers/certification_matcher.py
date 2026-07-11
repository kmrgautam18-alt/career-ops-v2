from backend.app.services.job_matching.models import MatchComponent


class CertificationMatcher:
    @staticmethod
    def match(
        candidate: list[str],
        required: list[str],
    ) -> MatchComponent:

        if not required:
            score = 100.0
            matched = []
            missing = []
        else:
            candidate_set = set(candidate)
            required_set = set(required)

            matched = sorted(candidate_set & required_set)
            missing = sorted(required_set - candidate_set)

            score = round(
                (len(matched) / len(required_set)) * 100,
                2,
            )

        return MatchComponent(
            score=score,
            matched=matched,
            missing=missing,
            reasons=[],
        )