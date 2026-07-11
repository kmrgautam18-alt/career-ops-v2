from backend.app.services.job_matching.matchers.education_matcher import (
    EducationMatcher,
)


def test_same_degree():
    result = EducationMatcher.match(
        candidate_degree="Bachelor",
        required_degree="Bachelor",
    )

    assert result.score == 100.0


def test_higher_degree():
    result = EducationMatcher.match(
        candidate_degree="Master",
        required_degree="Bachelor",
    )

    assert result.score == 100.0


def test_lower_degree():
    result = EducationMatcher.match(
        candidate_degree="Diploma",
        required_degree="Bachelor",
    )

    assert result.score == 50.0


def test_unknown_degree():
    result = EducationMatcher.match(
        candidate_degree="",
        required_degree="Bachelor",
    )

    assert result.score == 0.0