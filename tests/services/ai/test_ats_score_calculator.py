from backend.app.services.ai.ats.ats_score_calculator import (
    ATSScoreCalculator,
)


def test_ats_score_calculator():
    score = ATSScoreCalculator.calculate(
        keyword_score=80,
        formatting_score=60,
        section_score=100,
        readability_score=90,
    )

    assert score == 82.0