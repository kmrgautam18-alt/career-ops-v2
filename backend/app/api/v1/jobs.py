from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.schemas.job_schema import JobCreate

from backend.app.services.job_service import (
    list_jobs,
    list_jobs_paginated,
    add_job,
    get_job,
    update_existing_job,
    delete_existing_job,
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("")
def get_jobs(
    page: int | None = Query(default=None, ge=1),
    size: int | None = Query(default=None, ge=1, le=100),
    db: Session = Depends(get_db),
):

    if page is not None and size is not None:
        return list_jobs_paginated(
            db=db,
            page=page,
            size=size,
        )

    return list_jobs(db)


@router.post("")
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
):
    return add_job(db, job)


@router.get("/{job_id}")
def get_single_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    return get_job(db, job_id)


@router.put("/{job_id}")
def update_job_route(
    job_id: int,
    job: JobCreate,
    db: Session = Depends(get_db),
):
    return update_existing_job(
        db,
        job_id,
        job,
    )


@router.delete("/{job_id}")
def delete_job_route(
    job_id: int,
    db: Session = Depends(get_db),
):
    return delete_existing_job(
        db,
        job_id,
    )