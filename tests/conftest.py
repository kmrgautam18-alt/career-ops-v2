import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.database.init_db import init_database
from backend.app.database.session import SessionLocal
from backend.app.main import app


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Ensure all tables exist before tests run and seed test user."""
    init_database()

    # Seed the test user
    from backend.app.models.user import User
    from backend.app.security.password import hash_password

    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == "careerops@test.com").first()
        if not user:
            user = User(
                email="careerops@test.com",
                username="careerops",
                full_name="Career Ops",
                hashed_password=hash_password("CareerOps@123"),
                is_active=True,
                is_verified=True,
            )
            session.add(user)
            session.commit()
    finally:
        session.close()

    yield


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
