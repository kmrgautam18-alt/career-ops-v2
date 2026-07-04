from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.security.dependencies import (
    get_current_active_user,
)
from backend.app.services.dashboard_service import (
    get_dashboard_statistics,
    get_dashboard_status_summary,
    get_recent_dashboard_applications,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/health")
def health():
    """
    Dashboard health endpoint.
    """

    return {
        "status": "ok",
    }


@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Return dashboard statistics.
    """

    return get_dashboard_statistics(
        db=db,
        user_id=current_user.id,
    )


@router.get("/recent-applications")
def recent_applications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Return recent applications.
    """

    return get_recent_dashboard_applications(
        db=db,
        user_id=current_user.id,
    )


@router.get("/application-status")
def application_status(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Return application status summary.
    """

    return get_dashboard_status_summary(
        db=db,
        user_id=current_user.id,
    )