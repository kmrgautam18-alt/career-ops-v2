from backend.app.services.ai.ats.ats_engine import ATSEngine


def test_ats_engine():
    report = ATSEngine.evaluate(
        resume_text="""
Summary

Python Developer

Experience

Worked on Docker and Linux.

Skills

Python
Docker
Git
""",
        required_keywords=[
            "Python",
            "Docker",
            "Terraform",
        ],
    )

    # Overall score
    assert report.score.overall > 0

    # Keyword score
    assert report.score.keywords > 0

    # Formatting score
    assert report.score.formatting >= 0

    # Section score
    assert report.score.sections > 0

    # Missing keyword recommendation
    assert any(
        "Terraform" in recommendation.title
        for recommendation in report.recommendations
    )