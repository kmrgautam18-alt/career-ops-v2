from sqlalchemy.orm import Session

from backend.app.repositories.dashboard_repository_sa import (
    count_applications,
    count_applications_by_status,
    count_jobs,
    count_resumes,
    get_latest_resume,
    get_recent_applications,
    get_recent_jobs,
)
from backend.app.schemas.application_schema import ApplicationResponse
from backend.app.schemas.common_schema import ApiResponse
from backend.app.schemas.dashboard_schema import (
    DashboardStats,
    StatusCount,
)
from backend.app.schemas.job_schema import JobResponse
from backend.app.schemas.resume_schema import ResumeResponse


def get_dashboard_statistics(
    db: Session,
):
    """
    Return overall dashboard statistics.
    """

    stats = DashboardStats(
        total_jobs=count_jobs(db),
        total_applications=count_applications(db),
        total_resumes=count_resumes(db),
        applied=count_applications_by_status(db, "Applied"),
        interviews=count_applications_by_status(db, "Interview"),
        offers=count_applications_by_status(db, "Offer"),
        rejections=count_applications_by_status(db, "Rejected"),
    )

    return ApiResponse(
        success=True,
        message="Dashboard statistics retrieved successfully.",
        data=stats,
    )


def get_recent_dashboard_applications(
    db: Session,
):
    """
    Return recent applications.
    """

    applications = get_recent_applications(db)

    return ApiResponse(
        success=True,
        message="Recent applications retrieved successfully.",
        data=[
            ApplicationResponse.model_validate(application)
            for application in applications
        ],
    )


def get_recent_dashboard_jobs(
    db: Session,
):
    """
    Return recent jobs.
    """

    jobs = get_recent_jobs(db)

    return ApiResponse(
        success=True,
        message="Recent jobs retrieved successfully.",
        data=[JobResponse.model_validate(job) for job in jobs],
    )


def get_dashboard_status_summary(
    db: Session,
):
    """
    Return application status counts.
    """

    summary = [
        StatusCount(
            status="Applied",
            count=count_applications_by_status(
                db,
                "Applied",
            ),
        ),
        StatusCount(
            status="Interview",
            count=count_applications_by_status(
                db,
                "Interview",
            ),
        ),
        StatusCount(
            status="Offer",
            count=count_applications_by_status(
                db,
                "Offer",
            ),
        ),
        StatusCount(
            status="Rejected",
            count=count_applications_by_status(
                db,
                "Rejected",
            ),
        ),
    ]

    return ApiResponse(
        success=True,
        message="Application status summary retrieved successfully.",
        data=summary,
    )


def get_dashboard_resume_summary(
    db: Session,
):
    """
    Return latest uploaded resume.
    """

    resume = get_latest_resume(db)

    return ApiResponse(
        success=True,
        message="Latest resume retrieved successfully.",
        data=(ResumeResponse.model_validate(resume) if resume is not None else None),
    )
