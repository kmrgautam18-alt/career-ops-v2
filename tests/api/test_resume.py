from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def login():
    """
    Login test user and return JWT token.
    """

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "careerops@test.com",
            "password": "CareerOps@123",
        },
    )

    assert response.status_code == 200

    return response.json()["data"]["access_token"]


def upload_resume(token: str):
    """
    Upload a resume and return response body.
    """

    resume_path = Path("test-data/resume.pdf")

    assert resume_path.exists()

    with open(resume_path, "rb") as resume:
        response = client.post(
            "/api/v1/resumes/upload",
            headers={
                "Authorization": f"Bearer {token}",
            },
            data={
                "title": "Pytest Resume",
            },
            files={
                "file": (
                    "resume.pdf",
                    resume,
                    "application/pdf",
                ),
            },
        )

    assert response.status_code == 200

    return response.json()


def test_resume_list_requires_authentication():
    """
    Resume endpoint must reject anonymous users.
    """

    response = client.get("/api/v1/resumes")

    assert response.status_code == 401


def test_resume_upload():
    """
    Upload a resume successfully.
    """

    token = login()

    body = upload_resume(token)

    assert body["success"] is True
    assert body["data"]["title"] == "Pytest Resume"
    assert body["data"]["original_filename"] == "resume.pdf"
    assert body["data"]["upload_status"] == "UPLOADED"


def test_resume_list_after_upload():
    """
    Uploaded resume should appear in resume list.
    """

    token = login()

    upload_resume(token)

    response = client.get(
        "/api/v1/resumes",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert isinstance(body["data"], list)
    assert len(body["data"]) >= 1

    latest_resume = body["data"][0]

    assert "id" in latest_resume
    assert "title" in latest_resume
    assert "file_path" in latest_resume
    assert "stored_filename" in latest_resume
    assert "upload_status" in latest_resume

    assert latest_resume["upload_status"] == "UPLOADED"


def test_get_resume_by_id():
    """
    Retrieve a resume by its ID.
    """

    token = login()

    upload_body = upload_resume(token)

    resume_id = upload_body["data"]["id"]

    response = client.get(
        f"/api/v1/resumes/{resume_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["id"] == resume_id
    assert body["data"]["title"] == "Pytest Resume"
    assert body["data"]["original_filename"] == "resume.pdf"
    assert body["data"]["upload_status"] == "UPLOADED"


def test_resume_rename():
    """
    Rename an existing resume.
    """

    token = login()

    upload_body = upload_resume(token)

    resume_id = upload_body["data"]["id"]

    response = client.patch(
        f"/api/v1/resumes/{resume_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Senior DevOps Resume",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Resume renamed successfully."
    assert body["data"]["id"] == resume_id
    assert body["data"]["title"] == "Senior DevOps Resume"

    response = client.get(
        f"/api/v1/resumes/{resume_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["title"] == "Senior DevOps Resume"


def test_resume_delete():
    """
    Delete an existing resume.
    """

    token = login()

    upload_body = upload_resume(token)

    resume_id = upload_body["data"]["id"]

    response = client.delete(
        f"/api/v1/resumes/{resume_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Resume deleted successfully."
    assert body["data"]["resume_id"] == resume_id

    response = client.get(
        f"/api/v1/resumes/{resume_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False


def test_resume_not_found():
    """
    Requesting a non-existing resume should return 404.
    """

    token = login()

    response = client.get(
        "/api/v1/resumes/999999",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert "not found" in body["message"].lower()


def test_delete_already_deleted_resume():
    """
    Deleting an already deleted resume should return 404.
    """

    token = login()

    upload_body = upload_resume(token)

    resume_id = upload_body["data"]["id"]

    # First delete
    response = client.delete(
        f"/api/v1/resumes/{resume_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True

    # Second delete
    response = client.delete(
        f"/api/v1/resumes/{resume_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert "not found" in body["message"].lower()