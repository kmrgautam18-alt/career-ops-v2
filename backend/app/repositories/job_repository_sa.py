from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.job import Job
from backend.app.schemas.query_schema import (
    SortField,
    SortOrder,
)


def get_all_jobs(db: Session) -> list[Job]:
    """
    Return all jobs.
    """

    return (
        db.scalars(
            select(Job).order_by(Job.id)
        )
        .all()
    )


def get_jobs_paginated(
    db: Session,
    page: int,
    size: int,
    search: str | None = None,
    company: str | None = None,
    status: str | None = None,
    sort: SortField = SortField.id,
    order: SortOrder = SortOrder.asc,
):
    """
    Return paginated jobs with filtering.
    """

    query = select(Job)

    if search:
        query = query.where(
            Job.company.ilike(f"%{search}%")
            | Job.title.ilike(f"%{search}%")
        )

    if company:
        query = query.where(
            Job.company.ilike(f"%{company}%")
        )

    if status:
        query = query.where(
            Job.status == status.upper()
        )

    total = db.scalar(
        select(func.count()).select_from(
            query.subquery()
        )
    )

    sort_mapping = {
        SortField.id: Job.id,
        SortField.company: Job.company,
        SortField.job_title: Job.title,
        SortField.status: Job.status,
    }

    sort_column = sort_mapping[sort]

    if order == SortOrder.desc:
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    jobs = db.scalars(
        query.offset((page - 1) * size).limit(size)
    ).all()

    return jobs, total


def create_job(
    db: Session,
    company: str,
    title: str,
    url: str,
) -> Job:
    """
    Create a job.
    """

    job = Job(
        company=company,
        title=title,
        url=url,
        status="NEW",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_job_by_id(
    db: Session,
    job_id: int,
) -> Job | None:
    """
    Return job by ID.
    """

    return db.get(Job, job_id)


def update_job(
    db: Session,
    job: Job,
) -> Job:
    """
    Persist changes.
    """

    db.commit()
    db.refresh(job)

    return job


def delete_job(
    db: Session,
    job: Job,
) -> None:
    """
    Delete a job.
    """

    db.delete(job)
    db.commit()