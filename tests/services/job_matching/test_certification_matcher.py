from backend.app.services.job_matching.matchers.certification_matcher import (
    CertificationMatcher,
)


def test_full_match():
    result = CertificationMatcher.match(
        candidate=["AZ-104", "CKA"],
        required=["AZ-104"],
    )

    assert result.score == 100.0


def test_partial_match():
    result = CertificationMatcher.match(
        candidate=["CKA"],
        required=["AZ-104", "CKA"],
    )

    assert result.score == 50.0


def test_no_match():
    result = CertificationMatcher.match(
        candidate=[],
        required=["AZ-104"],
    )

    assert result.score == 0.0


def test_no_requirement():
    result = CertificationMatcher.match(
        candidate=[],
        required=[],
    )

    assert result.score == 100.0