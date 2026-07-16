from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.repositories.resume_repository_sa import (
    get_resume_by_id_and_user,
)
from backend.app.schemas.job_match_schema import JobMatchResponse
from backend.app.schemas.job_schema import JobCreate
from backend.app.schemas.query_schema import (
    SortField,
    SortOrder,
)
from backend.app.security.dependencies import (
    get_current_active_user,
)
from backend.app.services.job_matching.job_match_service import (
    match_job,
)
from backend.app.services.job_service import (
    add_job,
    delete_existing_job,
    get_job,
    list_jobs,
    list_jobs_paginated,
    update_existing_job,
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.get("/health")
def health():
    """
    Health endpoint.
    """

    return {
        "status": "ok",
    }


@router.get("")
def get_jobs(
    page: int | None = Query(default=None, ge=1),
    size: int | None = Query(default=None, ge=1, le=100),
    search: str | None = Query(default=None),
    company: str | None = Query(default=None),
    status: str | None = Query(default=None),
    sort: SortField = Query(default=SortField.id),
    order: SortOrder = Query(default=SortOrder.asc),
    db: Session = Depends(get_db),
):
    """
    Return jobs.
    """

    if page is not None and size is not None:
        return list_jobs_paginated(
            db=db,
            page=page,
            size=size,
            search=search,
            company=company,
            status=status,
            sort=sort,
            order=order,
        )

    if search or company or status:
        return list_jobs_paginated(
            db=db,
            page=1,
            size=1000,
            search=search,
            company=company,
            status=status,
            sort=sort,
            order=order,
        )

    if sort != SortField.id or order != SortOrder.asc:
        return list_jobs_paginated(
            db=db,
            page=1,
            size=1000,
            sort=sort,
            order=order,
        )

    return list_jobs(db)


@router.post("")
def create_job_endpoint(
    job: JobCreate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Create a new job.
    """

    return add_job(
        db=db,
        job=job,
    )


@router.get("/{job_id}")
def get_job_endpoint(
    job_id: int,
    db: Session = Depends(get_db),
):
    """
    Return a single job.
    """

    return get_job(
        db=db,
        job_id=job_id,
    )


@router.patch("/{job_id}")
def update_job_endpoint(
    job_id: int,
    job: JobCreate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Update a job.
    """

    return update_existing_job(
        db=db,
        job_id=job_id,
        job=job,
    )


@router.delete("/{job_id}")
def delete_job_endpoint(
    job_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Delete a job.
    """

    return delete_existing_job(
        db=db,
        job_id=job_id,
    )


@router.post(
    "/{job_id}/match/{resume_id}",
    response_model=JobMatchResponse,
)
def match_job_endpoint(
    job_id: int,
    resume_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Match the authenticated user's resume against a job.
    """

    resume = get_resume_by_id_and_user(
        db=db,
        resume_id=resume_id,
        user_id=current_user.id,
    )

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    try:
        return match_job(
            db=db,
            resume_id=resume_id,
            job_id=job_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate job match.",
        ) from exc