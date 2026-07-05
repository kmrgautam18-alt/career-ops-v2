from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.application import Application
from backend.app.models.job import Job
from backend.app.models.resume import Resume


def count_jobs(
    db: Session,
) -> int:
    """
    Return total number of jobs.
    """

    return db.scalar(
        select(func.count()).select_from(Job)
    ) or 0


def count_applications(
    db: Session,
) -> int:
    """
    Return total number of applications.
    """

    return db.scalar(
        select(func.count()).select_from(Application)
    ) or 0


def count_resumes(
    db: Session,
) -> int:
    """
    Return total number of resumes.
    """

    return db.scalar(
        select(func.count()).select_from(Resume)
    ) or 0


def count_applications_by_status(
    db: Session,
    status: str,
) -> int:
    """
    Return number of applications by status.
    """

    return db.scalar(
        select(func.count())
        .select_from(Application)
        .where(Application.status == status)
    ) or 0


def get_recent_jobs(
    db: Session,
    limit: int = 5,
) -> list[Job]:
    """
    Return most recently created jobs.
    """

    return (
        db.scalars(
            select(Job)
            .order_by(Job.created_at.desc())
            .limit(limit)
        )
        .all()
    )


def get_recent_applications(
    db: Session,
    limit: int = 5,
) -> list[Application]:
    """
    Return most recent applications.
    """

    return (
        db.scalars(
            select(Application)
            .order_by(Application.created_at.desc())
            .limit(limit)
        )
        .all()
    )


def get_latest_resume(
    db: Session,
) -> Resume | None:
    """
    Return the most recently uploaded resume.
    """

    return db.scalar(
        select(Resume)
        .order_by(Resume.created_at.desc())
        .limit(1)
    )