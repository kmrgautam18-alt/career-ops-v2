from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_ats_score_api():
    response = client.post(
        "/api/v1/ai/ats-score",
        json={
            "resume_text": """
Summary

Python Developer

Experience

Worked with Docker Linux Git.

Skills

Python
Docker
Git
""",
            "required_keywords": [
                "Python",
                "Docker",
                "Terraform",
            ],
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "score" in body
    assert "recommendations" in body

    assert body["score"]["overall"] > 0
    assert body["score"]["keywords"] > 0

    assert any(
        "Terraform" in recommendation["title"]
        for recommendation in body["recommendations"]
    )


def test_resume_optimizer_api():
    response = client.post(
        "/api/v1/ai/resume-optimize",
        json={
            "resume_text": """
Summary

Python Developer

Experience

Worked with Docker Linux Git.

Skills

Python
Docker
Git
""",
            "required_keywords": [
                "Python",
                "Terraform",
            ],
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "ats_score_before" in body
    assert "ats_score_after" in body
    assert "missing_keywords" in body
    assert "suggestions" in body

    assert body["ats_score_before"] > 0
    assert body["ats_score_after"] >= body["ats_score_before"]

    assert "Terraform" in body["missing_keywords"]

    assert len(body["suggestions"]) > 0

    assert any(
        suggestion["priority"] == "HIGH"
        for suggestion in body["suggestions"]
    )