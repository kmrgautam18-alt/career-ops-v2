from backend.app.repositories.job_repository import (
    get_all_jobs,
    create_job,
    get_job_by_id,
    update_job,
    delete_job,
)


def list_jobs():

    jobs = get_all_jobs()

    return {
        "count": len(jobs),
        "jobs": jobs
    }


def add_job(job):

    job_id = create_job(
        company=job.company,
        title=job.title,
        url=job.url
    )

    return {
        "message": "Job created successfully.",
        "job_id": job_id
    }


def get_job(job_id):

    job = get_job_by_id(job_id)

    if job is None:
        return {
            "message": "Job not found"
        }

    return job

def update_existing_job(job_id, job):

    updated = update_job(
        job_id=job_id,
        company=job.company,
        title=job.title,
        url=job.url
    )

    if updated == 0:
        return {
            "message": "Job not found"
        }

    return {
        "message": "Job updated successfully."
    }

def delete_existing_job(job_id):

    deleted = delete_job(job_id)

    if deleted == 0:
        return {
            "message": "Job not found"
        }

    return {
        "message": "Job deleted successfully."
    }
