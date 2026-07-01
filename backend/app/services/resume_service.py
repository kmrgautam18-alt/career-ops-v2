from pathlib import Path

from sqlalchemy.orm import Session

from backend.app.exceptions.resume_exceptions import (
    ResumeNotFoundException,
)
from backend.app.repositories.resume_repository_sa import (
    delete_resume,
    get_resume_by_id_and_user,
    get_resumes_by_user,
)
from backend.app.schemas.common_schema import ApiResponse
from backend.app.schemas.resume_schema import ResumeResponse
from backend.app.utils.file_storage import (
    delete_uploaded_file,
)


def list_user_resumes(
    db: Session,
    current_user,
):
    """
    Return all resumes belonging to the authenticated user.
    """

    resumes = get_resumes_by_user(
        db=db,
        user_id=current_user.id,
    )

    return ApiResponse(
        success=True,
        message="Resumes retrieved successfully.",
        data=[
            ResumeResponse.model_validate(resume)
            for resume in resumes
        ],
    )


def get_user_resume(
    db: Session,
    current_user,
    resume_id: int,
):
    """
    Return a single resume owned by the authenticated user.
    """

    resume = get_resume_by_id_and_user(
        db=db,
        resume_id=resume_id,
        user_id=current_user.id,
    )

    if resume is None:
        raise ResumeNotFoundException(resume_id)

    return ApiResponse(
        success=True,
        message="Resume retrieved successfully.",
        data=ResumeResponse.model_validate(resume),
    )


def delete_user_resume(
    db: Session,
    current_user,
    resume_id: int,
):
    """
    Delete a resume owned by the authenticated user.

    Steps:
        1. Verify ownership.
        2. Delete physical file.
        3. Delete database record.
    """

    resume = get_resume_by_id_and_user(
        db=db,
        resume_id=resume_id,
        user_id=current_user.id,
    )

    if resume is None:
        raise ResumeNotFoundException(resume_id)

    # Delete physical file (ignore if already missing)
    delete_uploaded_file(
        Path(resume.file_path)
    )

    # Delete database record
    delete_resume(
        db=db,
        resume=resume,
    )

    return ApiResponse(
        success=True,
        message="Resume deleted successfully.",
        data={
            "resume_id": resume_id,
        },
    )