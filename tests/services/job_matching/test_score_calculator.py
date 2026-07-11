from backend.app.services.job_matching.score_calculator import ScoreCalculator


def test_score_calculator():
    score = ScoreCalculator.calculate(
        skill=100,
        experience=80,
        education=90,
        certification=100,
        keyword=70,
        location=100,
    )

    assert score == 92.0