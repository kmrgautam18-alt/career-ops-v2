from backend.app.services.job_matching.explainability import (
    ExplainabilityEngine,
)


def test_explanations():
    reasons = ExplainabilityEngine.generate(
        matched_skills=["Python", "Docker"],
        missing_skills=["Terraform"],
    )

    assert "Matched skill: Python" in reasons
    assert "Matched skill: Docker" in reasons
    assert "Missing skill: Terraform" in reasons