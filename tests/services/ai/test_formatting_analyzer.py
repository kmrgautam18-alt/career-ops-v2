from backend.app.services.ai.ats.formatting_analyzer import (
    FormattingAnalyzer,
)


def test_formatting_analyzer():
    score, recommendations = FormattingAnalyzer.analyze(
        "Python Developer"
    )

    assert score == 40.0
    assert len(recommendations) == 3
    assert "Resume appears too short." in recommendations
    assert "Use bullet points for achievements." in recommendations
    assert "Add more professional details." in recommendations