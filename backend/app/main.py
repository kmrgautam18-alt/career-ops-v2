from fastapi import FastAPI
from backend.app.database.db import get_connection
from pydantic import BaseModel
from backend.app.services.job_service import (
    list_jobs,
    add_job,
    get_job,
    update_existing_job,
)


class Job(BaseModel):
    company: str
    title: str
    url: str

app = FastAPI(
    title="Career-Ops v2",
    version="0.1.0"
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

@app.get("/jobs/{job_id}")
def get_single_job(job_id: int):
    return get_job(job_id)

@app.put("/jobs/{job_id}")
def update_job_route(job_id: int, job: Job):
    return update_existing_job(job_id, job)

@app.post("/jobs")
def create_job(job: Job):
    return add_job(job)


