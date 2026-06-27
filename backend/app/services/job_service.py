from sqlalchemy.orm import Session

from backend.app.exceptions.custom_exceptions import JobNotFoundException

from backend.app.repositories.job_repository_sa import (
    get_all_jobs,
    create_job,
    get_job_by_id,
    update_job,
    delete_job,
)


def list_jobs(db: Session):

    jobs = get_all_jobs(db)

    return {
        "count": len(jobs),
        "jobs": jobs,
    }


def add_job(db: Session, job):

    created_job = create_job(
        db=db,
        company=job.company,
        title=job.title,
        url=job.url,
    )

    return {
        "message": "Job created successfully.",
        "job_id": created_job.id,
    }


def get_job(db: Session, job_id: int):

    job = get_job_by_id(
        db=db,
        job_id=job_id,
    )

    if job is None:
        raise JobNotFoundException(job_id)

    return job


def update_existing_job(
    db: Session,
    job_id: int,
    job,
):

    updated_job = update_job(
        db=db,
        job_id=job_id,
        company=job.company,
        title=job.title,
        url=job.url,
    )

    if updated_job is None:
        raise JobNotFoundException(job_id)

    return {
        "message": "Job updated successfully.",
    }


def delete_existing_job(
    db: Session,
    job_id: int,
):

    deleted = delete_job(
        db=db,
        job_id=job_id,
    )

    if not deleted:
        raise JobNotFoundException(job_id)

    return {
        "message": "Job deleted successfully.",
    }
