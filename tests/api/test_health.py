from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_docs_endpoint():
    """
    Swagger UI should be accessible.
    """

    response = client.get("/docs")

    assert response.status_code == 200


def test_openapi_endpoint():
    """
    OpenAPI schema should be accessible.
    """

    response = client.get("/openapi.json")

    assert response.status_code == 200