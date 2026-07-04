from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.application import Application
from backend.app.models.job import Job
from backend.app.models.resume import Resume


def get_dashboard_stats(
    db: Session,
    user_id: int,
):
    """
    Retrieve dashboard statistics for the authenticated user.
    """

    total_jobs = db.scalar(
        select(func.count()).select_from(Job)
    ) or 0

    total_applications = db.scalar(
        select(func.count())
        .select_from(Application)
        .where(Application.user_id == user_id)
    ) or 0

    total_resumes = db.scalar(
        select(func.count())
        .select_from(Resume)
        .where(Resume.user_id == user_id)
    ) or 0

    interviews = db.scalar(
        select(func.count())
        .select_from(Application)
        .where(
            Application.user_id == user_id,
            Application.status == "Interview",
        )
    ) or 0

    offers = db.scalar(
        select(func.count())
        .select_from(Application)
        .where(
            Application.user_id == user_id,
            Application.status == "Offer",
        )
    ) or 0

    rejections = db.scalar(
        select(func.count())
        .select_from(Application)
        .where(
            Application.user_id == user_id,
            Application.status == "Rejected",
        )
    ) or 0

    pending = db.scalar(
        select(func.count())
        .select_from(Application)
        .where(
            Application.user_id == user_id,
            Application.status == "Applied",
        )
    ) or 0

    return {
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "total_resumes": total_resumes,
        "interviews": interviews,
        "offers": offers,
        "rejections": rejections,
        "pending": pending,
    }


def get_recent_applications(
    db: Session,
    user_id: int,
    limit: int = 10,
):
    """
    Retrieve the most recent applications for the authenticated user.
    """

    return db.scalars(
        select(Application)
        .where(Application.user_id == user_id)
        .order_by(Application.created_at.desc())
        .limit(limit)
    ).all()


def get_application_status_summary(
    db: Session,
    user_id: int,
):
    """
    Retrieve application counts grouped by status.
    """

    rows = db.execute(
        select(
            Application.status,
            func.count(Application.id),
        )
        .where(Application.user_id == user_id)
        .group_by(Application.status)
        .order_by(Application.status)
    ).all()

    return [
        {
            "status": status,
            "count": count,
        }
        for status, count in rows
    ]