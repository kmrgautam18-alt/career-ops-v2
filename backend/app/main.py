from fastapi import FastAPI

from backend.app.database.db import get_connection

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
    version="0.1.0"
)

app.add_exception_handler(
    JobNotFoundException,
    job_not_found_exception_handler
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)

@app.get("/")
def root():
    return {
        "application": "Career-Ops v2",
        "status": "healthy"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/jobs")
def get_jobs():
    return list_jobs()

@app.get("/jobs/{job_id}")
def get_single_job(job_id: int):
    return get_job(job_id)

@app.put("/jobs/{job_id}")
def update_job_route(job_id: int, job: JobCreate):    
    return update_existing_job(job_id, job)

@app.delete("/jobs/{job_id}")
def delete_job_route(job_id: int):
    return delete_existing_job(job_id)

@app.post("/jobs")
def create_job(job: JobCreate):
    return add_job(job)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
