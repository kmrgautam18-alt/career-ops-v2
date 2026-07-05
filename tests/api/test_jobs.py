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


def test_job_requires_authentication():
    """
    Anonymous users cannot create jobs.
    """

    response = client.post(
        "/api/v1/jobs",
        json={
            "company": "Google",
            "title": "SRE",
            "url": "https://example.com",
        },
    )

    assert response.status_code == 401


def test_create_job():
    """
    Create a new job.
    """

    response = client.post(
        "/api/v1/jobs",
        headers=get_auth_headers(),
        json={
            "company": "Google",
            "title": "Site Reliability Engineer",
            "url": "https://careers.google.com/jobs/results/123456",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["company"] == "Google"
    assert body["data"]["status"] == "NEW"
def create_job() -> int:
    """
    Create a test job and return its ID.
    """

    response = client.post(
        "/api/v1/jobs",
        headers=get_auth_headers(),
        json={
            "company": "Google",
            "title": "Site Reliability Engineer",
            "url": "https://careers.google.com/jobs/results/123456",
        },
    )

    assert response.status_code == 200

    return response.json()["data"]["id"] 
def test_list_jobs():
    """
    Retrieve all jobs.
    """

    create_job()

    response = client.get(
        "/api/v1/jobs",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert isinstance(body["data"], list)
    assert len(body["data"]) >= 1

    latest_job = body["data"][0]

    assert "id" in latest_job
    assert "company" in latest_job
    assert "title" in latest_job
    assert "url" in latest_job
    assert "status" in latest_job

def test_get_job_by_id():
    """
    Retrieve a single job.
    """

    job_id = create_job()

    response = client.get(
        f"/api/v1/jobs/{job_id}",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["id"] == job_id
    assert body["data"]["company"] == "Google"
    assert body["data"]["title"] == "Site Reliability Engineer"
    assert body["data"]["status"] == "NEW"

def test_update_job():
    """
    Update an existing job.
    """

    job_id = create_job()

    response = client.patch(
        f"/api/v1/jobs/{job_id}",
        headers=get_auth_headers(),
        json={
            "company": "Google",
            "title": "Senior Site Reliability Engineer",
            "url": "https://careers.google.com/jobs/results/123456",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Job updated successfully."

    assert body["data"]["id"] == job_id
    assert body["data"]["company"] == "Google"
    assert (
        body["data"]["title"]
        == "Senior Site Reliability Engineer"
    )
    assert body["data"]["status"] == "NEW"

    response = client.get(
        f"/api/v1/jobs/{job_id}",
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["data"]["title"]
        == "Senior Site Reliability Engineer"
    )    

def test_delete_job():
    """
    Delete an existing job.
    """

    job_id = create_job()

    response = client.delete(
        f"/api/v1/jobs/{job_id}",
        headers=get_auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Job deleted successfully."
    assert body["data"]["job_id"] == job_id

    response = client.get(
        f"/api/v1/jobs/{job_id}",
    )

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["message"] == (
        f"Job with id {job_id} not found."
    )

def test_job_not_found():
    """
    Non-existing job should return 404.
    """

    # GET
    response = client.get(
        "/api/v1/jobs/999999",
    )

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["message"] == (
        "Job with id 999999 not found."
    )

    # PATCH
    response = client.patch(
        "/api/v1/jobs/999999",
        headers=get_auth_headers(),
        json={
            "company": "Google",
            "title": "Updated Job",
            "url": "https://example.com/job",
        },
    )

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["message"] == (
        "Job with id 999999 not found."
    )

    # DELETE
    response = client.delete(
        "/api/v1/jobs/999999",
        headers=get_auth_headers(),
    )

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["message"] == (
        "Job with id 999999 not found."
    )

def test_delete_already_deleted_job():
    """
    Deleting an already deleted job should return 404.
    """

    job_id = create_job()

    # First delete
    response = client.delete(
        f"/api/v1/jobs/{job_id}",
        headers=get_auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True

    # Second delete
    response = client.delete(
        f"/api/v1/jobs/{job_id}",
        headers=get_auth_headers(),
    )

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["message"] == (
        f"Job with id {job_id} not found."
    )    