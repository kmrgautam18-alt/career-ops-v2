from sqlalchemy.orm import Session

from backend.app.repositories.dashboard_repository_sa import (
    get_application_status_summary,
    get_dashboard_stats,
    get_recent_applications,
)
from backend.app.schemas.application_schema import ApplicationResponse
from backend.app.schemas.common_schema import ApiResponse
from backend.app.schemas.dashboard_schema import (
    DashboardStats,
    StatusCount,
)


def get_dashboard_statistics(
    db: Session,
    user_id: int,
):
    """
    Return dashboard statistics for the authenticated user.
    """

    stats = get_dashboard_stats(
        db=db,
        user_id=user_id,
    )

    return ApiResponse(
        success=True,
        message="Dashboard statistics retrieved successfully.",
        data=DashboardStats.model_validate(stats),
    )


def get_recent_dashboard_applications(
    db: Session,
    user_id: int,
):
    """
    Return recent applications for the authenticated user.
    """

    applications = get_recent_applications(
        db=db,
        user_id=user_id,
    )

    application_list = [
        ApplicationResponse.model_validate(application)
        for application in applications
    ]

    return ApiResponse(
        success=True,
        message="Recent applications retrieved successfully.",
        data=application_list,
    )


def get_dashboard_status_summary(
    db: Session,
    user_id: int,
):
    """
    Return application status summary for the authenticated user.
    """

    summary = get_application_status_summary(
        db=db,
        user_id=user_id,
    )

    status_summary = [
        StatusCount.model_validate(item)
        for item in summary
    ]

    return ApiResponse(
        success=True,
        message="Application status summary retrieved successfully.",
        data=status_summary,
    )