from backend.app.services.job_matching.matchers.keyword_matcher import (
    KeywordMatcher,
)


def test_exact_match():
    result = KeywordMatcher.match(
        resume="Python Docker Kubernetes Linux Git",
        job="Python Docker Kubernetes Linux Git",
    )

    assert result.score == 100.0


def test_partial_match():
    result = KeywordMatcher.match(
        resume="Python Docker Linux",
        job="Python Docker Kubernetes Git",
    )

    assert result.score == 50.0


def test_no_match():
    result = KeywordMatcher.match(
        resume="Java Spring",
        job="Python Docker Kubernetes",
    )

    assert result.score == 0.0