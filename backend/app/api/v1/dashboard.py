from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.security.dependencies import (
    get_current_active_user,
)
from backend.app.services.dashboard_service import (
    get_dashboard_resume_summary,
    get_dashboard_statistics,
    get_dashboard_status_summary,
    get_recent_dashboard_applications,
    get_recent_dashboard_jobs,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/health")
def health():
    """
    Dashboard health check.
    """

    return {
        "status": "ok",
    }


@router.get("")
def dashboard_summary(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Return dashboard statistics.
    """

    return get_dashboard_statistics(
        db=db,
    )


@router.get("/recent-applications")
def recent_applications(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Return recent applications.
    """

    return get_recent_dashboard_applications(
        db=db,
    )


@router.get("/recent-jobs")
def recent_jobs(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Return recent jobs.
    """

    return get_recent_dashboard_jobs(
        db=db,
    )


@router.get("/status-summary")
def status_summary(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Return application status summary.
    """

    return get_dashboard_status_summary(
        db=db,
    )


@router.get("/resume-summary")
def resume_summary(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Return latest uploaded resume.
    """

    return get_dashboard_resume_summary(
        db=db,
    )
