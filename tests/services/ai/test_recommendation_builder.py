from backend.app.services.ai.ats.recommendation_builder import (
    RecommendationBuilder,
)


def test_recommendation_builder():
    recommendations = RecommendationBuilder.build(
        missing_keywords=[
            "Terraform",
            "Kubernetes",
        ],
        missing_sections=[
            "Education",
        ],
        formatting_recommendations=[
            "Use bullet points.",
        ],
    )

    assert len(recommendations) == 4

    assert recommendations[0].title == "Add keyword: Terraform"
    assert recommendations[1].title == "Add keyword: Kubernetes"
    assert recommendations[2].title == "Add Education section"
    assert recommendations[3].title == "Formatting Improvement"

    assert recommendations[0].priority == "HIGH"
    assert recommendations[3].priority == "MEDIUM"