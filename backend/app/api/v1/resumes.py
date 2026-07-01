from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
)
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.security.dependencies import (
    get_current_active_user,
)
from backend.app.services.resume_service import (
    delete_user_resume,
    get_user_resume,
    list_user_resumes,
)
from backend.app.services.resume_upload_service import (
    upload_resume,
)

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


@router.post("/upload")
def upload_resume_endpoint(
    title: str = Form(...),
    file: UploadFile = File(...),
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Upload a new resume.
    """

    return upload_resume(
        db=db,
        user=current_user,
        title=title,
        upload_file=file,
    )


@router.get("")
def get_my_resumes(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Return all resumes belonging to the authenticated user.
    """

    return list_user_resumes(
        db=db,
        current_user=current_user,
    )


@router.get("/{resume_id}")
def get_resume(
    resume_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Return a single resume.
    """

    return get_user_resume(
        db=db,
        current_user=current_user,
        resume_id=resume_id,
    )


@router.delete("/{resume_id}")
def delete_resume_endpoint(
    resume_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Delete a resume.
    """

    return delete_user_resume(
        db=db,
        current_user=current_user,
        resume_id=resume_id,
    )