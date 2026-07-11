from backend.app.services.job_matching.matchers.location_matcher import (
    LocationMatcher,
)


def test_same_city():
    result = LocationMatcher.match(
        candidate="Bangalore",
        job="Bangalore",
        remote=False,
    )

    assert result.score == 100.0


def test_remote_job():
    result = LocationMatcher.match(
        candidate="Delhi",
        job="Bangalore",
        remote=True,
    )

    assert result.score == 100.0


def test_different_city():
    result = LocationMatcher.match(
        candidate="Delhi",
        job="Bangalore",
        remote=False,
    )

    assert result.score == 50.0