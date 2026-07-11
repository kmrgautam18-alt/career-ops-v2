from backend.app.services.job_matching.recommendation_engine import (
    RecommendationEngine,
)


def test_generate_recommendations():
    recommendations = RecommendationEngine.generate(
        missing_skills=[
            "Terraform",
            "Kubernetes",
        ],
        overall_score=72,
    )

    assert "Learn Terraform" in recommendations
    assert "Learn Kubernetes" in recommendations