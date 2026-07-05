import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal
from backend.app.main import app


@pytest.fixture(scope="session")
def client():
    """
    Shared FastAPI TestClient.
    """

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def db() -> Session:
    """
    Database session for tests.
    """

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def auth_headers(client):
    """
    Login as the default test user and return Authorization header.
    """

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "careerops@test.com",
            "password": "CareerOps@123",
        },
    )

    assert response.status_code == 200

    token = response.json()["data"]["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }