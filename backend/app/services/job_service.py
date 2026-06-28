from sqlalchemy.orm import Session

from backend.app.exceptions.custom_exceptions import JobNotFoundException

from backend.app.repositories.job_repository_sa import (
    get_all_jobs,
    create_job,
    get_job_by_id,
    update_job,
    delete_job,
)

from backend.app.schemas.common_schema import ApiResponse
from backend.app.schemas.job_schema import JobResponse


def list_jobs(db: Session):

    jobs = get_all_jobs(db)

    job_list = [
        JobResponse.model_validate(job)
        for job in jobs
    ]

    return ApiResponse(
        success=True,
        message="Jobs retrieved successfully.",
        data={
            "count": len(job_list),
            "jobs": job_list,
        },
    )


def add_job(db: Session, job):

    created_job = create_job(
        db=db,
        company=job.company,
        title=job.title,
        url=str(job.url),
    )

    return ApiResponse(
        success=True,
        message="Job created successfully.",
        data=JobResponse.model_validate(created_job),
    )


def get_job(db: Session, job_id: int):

    job = get_job_by_id(
        db=db,
        job_id=job_id,
    )

    if job is None:
        raise JobNotFoundException(job_id)

    return ApiResponse(
        success=True,
        message="Job retrieved successfully.",
        data=JobResponse.model_validate(job),
    )


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
        url=str(job.url),
    )

    if updated_job is None:
        raise JobNotFoundException(job_id)

    return ApiResponse(
        success=True,
        message="Job updated successfully.",
        data=JobResponse.model_validate(updated_job),
    )


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

    return ApiResponse(
        success=True,
        message="Job deleted successfully.",
        data={
            "job_id": job_id,
        },
    )