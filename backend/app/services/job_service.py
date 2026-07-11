from math import ceil

from sqlalchemy.orm import Session

from backend.app.exceptions.custom_exceptions import (
    JobNotFoundException,
)
from backend.app.repositories.job_repository_sa import (
    create_job,
    delete_job,
    get_all_jobs,
    get_job_by_id,
    get_jobs_paginated,
    update_job,
)
from backend.app.schemas.common_schema import (
    ApiResponse,
    Pagination,
)
from backend.app.schemas.job_schema import (
    JobCreate,
    JobResponse,
)
from backend.app.schemas.query_schema import (
    SortField,
    SortOrder,
)


def list_jobs(
    db: Session,
):
    """
    Return all jobs.
    """

    jobs = get_all_jobs(db)

    return ApiResponse(
        success=True,
        message="Jobs retrieved successfully.",
        data=[JobResponse.model_validate(job) for job in jobs],
    )


def list_jobs_paginated(
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
    Return paginated jobs.
    """

    jobs, total = get_jobs_paginated(
        db=db,
        page=page,
        size=size,
        search=search,
        company=company,
        status=status,
        sort=sort,
        order=order,
    )

    pagination = Pagination(
        page=page,
        size=size,
        total=total,
        pages=ceil(total / size) if total else 0,
    )

    return ApiResponse(
        success=True,
        message="Jobs retrieved successfully.",
        pagination=pagination,
        data=[JobResponse.model_validate(job) for job in jobs],
    )


def add_job(
    db: Session,
    job: JobCreate,
):
    """
    Create a job.
    """

    created_job = create_job(
    db=db,
    company=job.company,
    title=job.title,
    url=str(job.url),
    description=job.description,
)

    return ApiResponse(
        success=True,
        message="Job created successfully.",
        data=JobResponse.model_validate(
            created_job,
        ),
    )


def get_job(
    db: Session,
    job_id: int,
):
    """
    Return a job.
    """

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
    job: JobCreate,
):
    """
    Update an existing job.
    """

    existing = get_job_by_id(
        db=db,
        job_id=job_id,
    )

    if existing is None:
        raise JobNotFoundException(job_id)

    existing.company = job.company
    existing.title = job.title
    existing.url = str(job.url)
    existing.description = job.description

    updated = update_job(
        db=db,
        job=existing,
    )

    return ApiResponse(
        success=True,
        message="Job updated successfully.",
        data=JobResponse.model_validate(updated),
    )


def delete_existing_job(
    db: Session,
    job_id: int,
):
    """
    Delete a job.
    """

    job = get_job_by_id(
        db=db,
        job_id=job_id,
    )

    if job is None:
        raise JobNotFoundException(job_id)

    delete_job(
        db=db,
        job=job,
    )

    return ApiResponse(
        success=True,
        message="Job deleted successfully.",
        data={
            "job_id": job_id,
        },
    )
