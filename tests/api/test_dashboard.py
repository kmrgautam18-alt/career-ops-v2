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


def test_dashboard_requires_authentication():
    """
    Anonymous users must not access dashboard.
    """

    response = client.get("/api/v1/dashboard")

    assert response.status_code == 401


def test_dashboard_summary():
    """
    Retrieve dashboard statistics.
    """

    response = client.get(
        "/api/v1/dashboard",
        headers=get_auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == (
        "Dashboard statistics retrieved successfully."
    )

    data = body["data"]

    assert "total_jobs" in data
    assert "total_applications" in data
    assert "total_resumes" in data
    assert "applied" in data
    assert "interviews" in data
    assert "offers" in data
    assert "rejections" in data

def test_recent_jobs():
    """
    Retrieve recent jobs.
    """

    response = client.get(
        "/api/v1/dashboard/recent-jobs",
        headers=get_auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == (
        "Recent jobs retrieved successfully."
    )

    assert isinstance(body["data"], list)

    if body["data"]:
        job = body["data"][0]

        assert "id" in job
        assert "company" in job
        assert "title" in job
        assert "url" in job
        assert "status" in job

def test_recent_applications():
    """
    Retrieve recent applications.
    """

    response = client.get(
        "/api/v1/dashboard/recent-applications",
        headers=get_auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == (
        "Recent applications retrieved successfully."
    )

    assert isinstance(body["data"], list)

    if body["data"]:
        application = body["data"][0]

        assert "id" in application
        assert "job_id" in application
        assert "user_id" in application
        assert "status" in application
        assert "applied_date" in application

def test_status_summary():
    """
    Retrieve application status summary.
    """

    response = client.get(
        "/api/v1/dashboard/status-summary",
        headers=get_auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == (
        "Application status summary retrieved successfully."
    )

    summary = body["data"]

    assert isinstance(summary, list)
    assert len(summary) == 4

    expected = {
        "Applied",
        "Interview",
        "Offer",
        "Rejected",
    }

    returned = {item["status"] for item in summary}

    assert returned == expected

    for item in summary:
        assert isinstance(item["count"], int)
        assert item["count"] >= 0

def test_resume_summary():
    """
    Retrieve latest uploaded resume.
    """

    response = client.get(
        "/api/v1/dashboard/resume-summary",
        headers=get_auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == (
        "Latest resume retrieved successfully."
    )

    resume = body["data"]

    if resume is None:
        return

    assert "id" in resume
    assert "user_id" in resume
    assert "title" in resume
    assert "original_filename" in resume
    assert "stored_filename" in resume
    assert "file_path" in resume
    assert "upload_status" in resume

    assert resume["upload_status"] == "UPLOADED"        