from fastapi.testclient import TestClient

from backend.app.main import app
from tests.utils.auth_helper import login_and_get_token

client = TestClient(app)


def get_auth_headers() -> dict[str, str]:
    """
    Return authentication headers.
    """

    token = login_and_get_token(
        client=client,
        email="careerops@test.com",
        password="CareerOps@123",
    )

    return {
        "Authorization": f"Bearer {token}",
    }


def create_application() -> int:
    """
    Create a test application if it does not already exist.
    """

    response = client.post(
        "/api/v1/applications",
        headers=get_auth_headers(),
        json={
            "job_id": 1,
            "status": "Applied",
            "applied_date": "2026-07-05",
            "notes": "Applied from automated test",
        },
    )

    body = response.json()

    if body["success"]:
        return body["data"]["id"]

    response = client.get(
        "/api/v1/applications",
        headers=get_auth_headers(),
    )

    return response.json()["data"][0]["id"]


def test_application_requires_authentication():
    """
    Anonymous users must not access applications.
    """

    response = client.get("/api/v1/applications")

    assert response.status_code == 401


def test_create_application():
    """
    Create a new application.
    """

    response = client.post(
        "/api/v1/applications",
        headers=get_auth_headers(),
        json={
            "job_id": 1,
            "status": "Applied",
            "applied_date": "2026-07-05",
            "notes": "Applied from automated test",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] in [True, False]

    if body["success"]:
        assert body["data"]["job_id"] == 1
        assert body["data"]["status"] == "Applied"
    else:
        assert body["message"] == ("You have already applied for this job.")


def test_list_applications():
    """
    Retrieve all applications.
    """

    response = client.get(
        "/api/v1/applications",
        headers=get_auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert isinstance(body["data"], list)


def test_get_application_by_id():
    """
    Retrieve a single application.
    """

    application_id = create_application()

    response = client.get(
        f"/api/v1/applications/{application_id}",
        headers=get_auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["id"] == application_id


def test_update_application():
    """
    Update an existing application.
    """

    application_id = create_application()

    response = client.patch(
        f"/api/v1/applications/{application_id}",
        headers=get_auth_headers(),
        json={
            "status": "Interview",
            "notes": "Interview scheduled",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["id"] == application_id
    assert body["data"]["status"] == "Interview"
    assert body["data"]["notes"] == "Interview scheduled"


def test_delete_application():
    """
    Delete an existing application.
    """

    application_id = create_application()

    response = client.delete(
        f"/api/v1/applications/{application_id}",
        headers=get_auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Application deleted successfully."
    assert body["data"]["application_id"] == application_id


def test_application_not_found():
    """
    Non-existing application should return 404.
    """

    headers = get_auth_headers()

    # GET
    response = client.get(
        "/api/v1/applications/999999",
        headers=headers,
    )

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["message"] == ("Application with id 999999 not found.")

    # PATCH
    response = client.patch(
        "/api/v1/applications/999999",
        headers=headers,
        json={
            "status": "Interview",
        },
    )

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["message"] == ("Application with id 999999 not found.")

    # DELETE
    response = client.delete(
        "/api/v1/applications/999999",
        headers=headers,
    )

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["message"] == ("Application with id 999999 not found.")


def test_duplicate_application():
    """
    A user should not be able to apply for the same job twice.
    """

    headers = get_auth_headers()

    payload = {
        "job_id": 1,
        "status": "Applied",
        "applied_date": "2026-07-05",
        "notes": "Applied from automated test",
    }

    # Ensure an application already exists.
    client.post(
        "/api/v1/applications",
        headers=headers,
        json=payload,
    )

    # Try creating the same application again.
    response = client.post(
        "/api/v1/applications",
        headers=headers,
        json=payload,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is False
    assert body["message"] == ("You have already applied for this job.")
    assert body["data"] is None


def test_delete_already_deleted_application():
    """
    Deleting an already deleted application should return 404.
    """

    application_id = create_application()

    # First delete should succeed.
    response = client.delete(
        f"/api/v1/applications/{application_id}",
        headers=get_auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True

    # Second delete should return 404.
    response = client.delete(
        f"/api/v1/applications/{application_id}",
        headers=get_auth_headers(),
    )

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["message"] == (f"Application with id {application_id} not found.")
