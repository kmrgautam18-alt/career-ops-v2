from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.job import Job


def get_all_jobs(db: Session):
    """
    Retrieve all jobs from the database.
    """

    jobs = db.scalars(
        select(Job).order_by(Job.id)
    ).all()

    return jobs


def create_job(
    db: Session,
    company: str,
    title: str,
    url: str
):
    """
    Create a new job.
    """

    job = Job(
        company=company,
        title=title,
        url=url,
        status="NEW"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_job_by_id(
    db: Session,
    job_id: int
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
    url: str
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
    job_id: int
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
