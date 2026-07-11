from backend.app.services.job_matching.matchers.experience_matcher import (
    ExperienceMatcher,
)


def test_experience_matcher():
    result = ExperienceMatcher.match(
        candidate_years=5,
        required_years=4,
    )

    assert result.score == 100.0


def test_experience_partial():
    result = ExperienceMatcher.match(
        candidate_years=3,
        required_years=5,
    )

    assert result.score == 60.0


def test_experience_zero():
    result = ExperienceMatcher.match(
        candidate_years=0,
        required_years=5,
    )

    assert result.score == 0.0