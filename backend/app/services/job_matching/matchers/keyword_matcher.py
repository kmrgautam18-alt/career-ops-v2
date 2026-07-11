from backend.app.services.job_matching.models import MatchComponent


class KeywordMatcher:
    @staticmethod
    def match(
        resume: str,
        job: str,
    ) -> MatchComponent:

        resume_words = set(resume.lower().split())
        job_words = set(job.lower().split())

        if not job_words:
            score = 100.0
            matched = []
            missing = []
        else:
            matched = sorted(resume_words & job_words)
            missing = sorted(job_words - resume_words)

            score = round(
                (len(matched) / len(job_words)) * 100,
                2,
            )

        return MatchComponent(
            score=score,
            matched=matched,
            missing=missing,
            reasons=[],
        )