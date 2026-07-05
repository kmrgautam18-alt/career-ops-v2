from fastapi.testclient import TestClient


def login_and_get_token(
    client: TestClient,
    email: str,
    password: str,
) -> str:
    """
    Login and return JWT access token.
    """

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    body = response.json()

    return body["data"]["access_token"]
