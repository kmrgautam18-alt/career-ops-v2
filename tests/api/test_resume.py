from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_resume_list_requires_authentication():
    """
    Resume endpoint must reject anonymous users.
    """

    response = client.get("/api/v1/resumes")

    assert response.status_code == 401