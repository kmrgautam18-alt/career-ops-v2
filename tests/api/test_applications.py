from fastapi.testclient import TestClient

from backend.app.main import app
from tests.utils.auth_helper import login_and_get_token

client = TestClient(app)


def get_auth_headers() -> dict:
    token = login_and_get_token(
        client=client,
        email="careerops@test.com",
        password="CareerOps@123",
    )

    return {
        "Authorization": f"Bearer {token}",
    }


def test_applications_health():
    response = client.get("/api/v1/applications/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
    }


def test_get_all_applications():
    response = client.get(
        "/api/v1/applications",
        headers=get_auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "applications" in body["data"]