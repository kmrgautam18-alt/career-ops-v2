from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db

from backend.app.schemas.job_schema import JobCreate

from backend.app.exceptions.handlers import (
    global_exception_handler,
    job_not_found_exception_handler,
)

from backend.app.exceptions.custom_exceptions import JobNotFoundException

from backend.app.services.job_service import (
    list_jobs,
    add_job,
    get_job,
    update_existing_job,
    delete_existing_job,
)

app = FastAPI(
    title="Career-Ops v2",
    version="0.1.0",
)

app.add_exception_handler(
    JobNotFoundException,
    job_not_found_exception_handler,
)

app.add_exception_handler(
    Exception,
    global_exception_handler,
)


@app.get("/")
def root():
    return {
        "application": "Career-Ops v2",
        "status": "healthy",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/jobs")
def get_jobs(
    db: Session = Depends(get_db),
):
    return list_jobs(db)


@app.get("/jobs/{job_id}")
def get_single_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    return get_job(db, job_id)


@app.post("/jobs")
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
):
    return add_job(db, job)


@app.put("/jobs/{job_id}")
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


@app.delete("/jobs/{job_id}")
def delete_job_route(
    job_id: int,
    db: Session = Depends(get_db),
):
    return delete_existing_job(
        db,
        job_id,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
