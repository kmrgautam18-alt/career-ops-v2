from sqlalchemy import select, func
from sqlalchemy.orm import Session

from backend.app.models.job import Job
from backend.app.schemas.query_schema import (
    SortField,
    SortOrder,
)


def get_all_jobs(db: Session):
    """
    Retrieve all jobs from the database.
    """

    jobs = db.scalars(
        select(Job).order_by(Job.id)
    ).all()

    return jobs


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
    Retrieve paginated jobs with enterprise filtering and sorting.
    """

    query = select(Job)

    # Search
    if search:
        query = query.where(
            Job.company.ilike(f"%{search}%")
            | Job.title.ilike(f"%{search}%")
        )

    # Company Filter
    if company:
        query = query.where(
            Job.company.ilike(f"%{company}%")
        )

    # Status Filter
    if status:
        query = query.where(
            Job.status == status.upper()
        )

    total = db.scalar(
        select(func.count()).select_from(query.subquery())
    )

    sort_mapping = {
        SortField.id: Job.id,
        SortField.company: Job.company,
        SortField.title: Job.title,
        SortField.status: Job.status,
    }

    sort_column = sort_mapping[sort]

    if order == SortOrder.desc:
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    offset = (page - 1) * size

    jobs = db.scalars(
        query.offset(offset).limit(size)
    ).all()

    return jobs, total


def create_job(
    db: Session,
    company: str,
    title: str,
    url: str,
):
    """
    Create a new job.
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
):
    """
    Retrieve a single job by ID.
    """

    return db.get(Job, job_id)


def update_job(
    db: Session,
    job_id: int,
    company: str,
    title: str,
    url: str,
):
    """
    Update an existing job.
    """

    job = db.get(Job, job_id)

    if job is None:
        return None

    job.company = company
    job.title = title
    job.url = url

    db.commit()
    db.refresh(job)

    return job


def delete_job(
    db: Session,
    job_id: int,
):
    """
    Delete a job.
    """

    job = db.get(Job, job_id)

    if job is None:
        return False

    db.delete(job)
    db.commit()

    return True