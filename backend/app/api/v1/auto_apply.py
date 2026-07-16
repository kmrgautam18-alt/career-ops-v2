"""
Auto-Apply API Router.
Endpoints for the Auto Job Application Engine.
"""

from fastapi import APIRouter, Depends, HTTPException, Query

from backend.app.schemas.auto_application_schema import (
    AutoApplicationCreate,
    AutoApplicationUpdate,
    ResumeBuildRequest,
    ResumeBuildResponse,
    ScrapeJobRequest,
    ScrapeJobResponse,
)
from backend.app.security.dependencies import (
    get_current_active_user,
)
from backend.app.services.auto_apply_service import (
    create_auto_application,
    delete_auto_application,
    get_auto_application,
    get_dashboard_stats,
    list_auto_applications,
    record_interview,
    run_full_auto_apply,
    run_scrape,
    run_send_application,
    run_tailor_resume,
    schedule_followup,
    update_auto_application,
)

router = APIRouter(
    prefix="/auto-apply",
    tags=["Auto Apply"],
)


# ── Dashboard ──────────────────────────────────────────────────────────


@router.get("/dashboard", response_model=dict)
def get_auto_apply_dashboard(
    current_user=Depends(get_current_active_user),
):
    """Get auto-apply dashboard statistics."""
    stats = get_dashboard_stats(current_user.id)
    return {
        "success": True,
        "message": "Dashboard stats retrieved",
        "data": stats,
    }


# ── CRUD Auto-Applications ─────────────────────────────────────────────


@router.get("")
def list_auto_applications_endpoint(
    current_user=Depends(get_current_active_user),
):
    """List all auto-applications for the current user."""
    apps = list_auto_applications(current_user.id)
    return {
        "success": True,
        "message": f"Found {len(apps)} applications",
        "data": apps,
    }


@router.get("/{app_id}")
def get_auto_application_endpoint(
    app_id: int,
    current_user=Depends(get_current_active_user),
):
    """Get a single auto-application."""
    app = get_auto_application(app_id)
    if not app or app.get("user_id") != current_user.id:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "success": True,
        "message": "Application retrieved",
        "data": app,
    }


@router.post("")
def create_auto_application_endpoint(
    data: AutoApplicationCreate,
    current_user=Depends(get_current_active_user),
):
    """Create a new auto-application entry (manually add a job to apply to)."""
    app = create_auto_application(current_user.id, data)
    return {
        "success": True,
        "message": f"Sourced job at {data.company}",
        "data": app,
    }


@router.patch("/{app_id}")
def update_auto_application_endpoint(
    app_id: int,
    data: AutoApplicationUpdate,
    current_user=Depends(get_current_active_user),
):
    """Update an auto-application (status, interview details, notes)."""
    updated = update_auto_application(app_id, current_user.id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "success": True,
        "message": "Application updated",
        "data": updated,
    }


@router.delete("/{app_id}")
def delete_auto_application_endpoint(
    app_id: int,
    current_user=Depends(get_current_active_user),
):
    """Delete an auto-application."""
    deleted = delete_auto_application(app_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "success": True,
        "message": "Application deleted",
    }


# ── Scrape Jobs ────────────────────────────────────────────────────────


@router.post("/scrape", response_model=ScrapeJobResponse)
def scrape_jobs_endpoint(
    req: ScrapeJobRequest,
    current_user=Depends(get_current_active_user),
):
    """Scrape jobs from LinkedIn, Indeed, or company career pages."""
    scraped = run_scrape(
        source=req.source,
        query=req.query,
        location=req.location,
        max_results=req.max_results,
    )
    return {
        "success": True,
        "source": req.source,
        "count": len(scraped),
        "jobs": [j.model_dump() for j in scraped],
    }


# ── Pipeline Actions ───────────────────────────────────────────────────


@router.post("/{app_id}/optimize", response_model=ResumeBuildResponse)
def optimize_resume_for_job(
    app_id: int,
    req: ResumeBuildRequest | None = None,
    current_user=Depends(get_current_active_user),
):
    """Step 2: AI-optimize the resume for a specific job application."""
    # For now, we pass an empty template (auto_apply_service has a default)
    result = run_tailor_resume(
        app_id=app_id,
        user_id=current_user.id,
        resume_json="",
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return {
        "success": True,
        "message": result["message"],
        "ats_score": result.get("ats_score"),
        "data": {
            "professional_summary": result.get("professional_summary", ""),
            "missing_keywords": result.get("missing_keywords", []),
        },
    }


@router.post("/{app_id}/send")
def send_application_email_endpoint(
    app_id: int,
    hr_email: str | None = Query(None, description="HR email address"),
    current_user=Depends(get_current_active_user),
):
    """Step 3: Send the application email."""
    result = run_send_application(
        app_id=app_id,
        user_id=current_user.id,
        hr_email=hr_email,
    )
    return {
        "success": result["success"],
        "message": result["message"],
    }


@router.post("/{app_id}/followup")
def send_followup_endpoint(
    app_id: int,
    current_user=Depends(get_current_active_user),
):
    """Send a follow-up email for an application."""
    result = schedule_followup(app_id=app_id, user_id=current_user.id)
    return result


@router.post("/{app_id}/interview")
def record_interview_endpoint(
    app_id: int,
    interview_date: str = Query(..., description="Interview date (ISO format)"),
    interview_type: str = Query("video", description="phone, video, onsite"),
    current_user=Depends(get_current_active_user),
):
    """Record an interview for an application."""
    result = record_interview(
        app_id=app_id,
        user_id=current_user.id,
        interview_date=interview_date,
        interview_type=interview_type,
    )
    return result


@router.post("/full-pipeline")
def run_full_auto_apply_pipeline(
    source: str = Query(..., description="linkedin, indeed, company_career, all"),
    query: str = Query(..., description="Job search query"),
    location: str | None = Query(None),
    max_results: int = Query(3, description="Max jobs to process"),
    current_user=Depends(get_current_active_user),
):
    """
    Run the complete auto-apply pipeline:
    1. Scrape jobs → 2. Save → 3. AI tailor resume → 4. Send email
    """
    results = run_full_auto_apply(
        user_id=current_user.id,
        source=source,
        query=query,
        location=location,
        max_results=max_results,
    )
    return {
        "success": True,
        "message": f"Processed {len(results)} applications",
        "data": results,
    }


# ── Resume Templates (placeholder — extend later) ──────────────────────


@router.get("/templates")
def list_resume_templates(
    current_user=Depends(get_current_active_user),
):
    """List resume templates (placeholder)."""
    return {
        "success": True,
        "message": "Resume templates list",
        "data": [
            {
                "id": 0,
                "name": "Default Template",
                "is_default": True,
                "skills": "Python, TypeScript, React, FastAPI, PostgreSQL, Docker, AWS, Git, Kubernetes, CI/CD",
                "experience": "Senior full-stack developer with 5+ years experience building scalable web applications...",
                "education": "B.S. Computer Science",
            }
        ],
    }
