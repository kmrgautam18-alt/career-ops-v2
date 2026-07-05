from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_login_invalid_credentials():
    """
    Invalid credentials should return HTTP 401.
    """

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "invalid@example.com",
            "password": "WrongPassword123",
        },
    )

    assert response.status_code == 401
