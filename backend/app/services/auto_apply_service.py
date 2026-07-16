"""
Auto-Apply Orchestrator Service.
Coordinates the full pipeline: scrape → AI tailor resume → send email → track status.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from typing import Any

from backend.app.core.config import settings
from backend.app.schemas.auto_application_schema import (
    AutoApplicationCreate,
    AutoApplicationUpdate,
    ScrapedJobItem,
)
from backend.app.services.email_service import (
    send_application_email,
    send_followup_email,
)
from backend.app.services.job_scraper_service import scrape_jobs
from backend.app.services.resume_builder_service import (
    build_full_resume_text,
    generate_cover_letter,
    tailor_resume,
)
from backend.app.services.webhook_service import notify_application_updated

logger = logging.getLogger(__name__)

# ── In-memory store (simulated repository) ─────────────────────────────
# TODO: Replace with proper CRUD repository

_auto_applications: dict[int, dict[str, Any]] = {}
_auto_applications_counter = 0

_STORE_FILE = "data/auto_applications.json"


def _load_store() -> dict[int, dict[str, Any]]:
    global _auto_applications
    try:
        import json
        import os
        if os.path.exists(_STORE_FILE):
            with open(_STORE_FILE) as f:
                data = json.load(f)
                _auto_applications = {int(k): v for k, v in data.items()}
    except Exception as e:
        logger.warning("Could not load auto-app store: %s", e)
    return _auto_applications


def _save_store() -> None:
    global _auto_applications
    try:
        import json
        import os
        os.makedirs(os.path.dirname(_STORE_FILE) or ".", exist_ok=True)
        with open(_STORE_FILE, "w") as f:
            json.dump(_auto_applications, f, default=str, indent=2)
    except Exception as e:
        logger.warning("Could not save auto-app store: %s", e)


def _next_id() -> int:
    global _auto_applications_counter
    _auto_applications_counter += 1
    return _auto_applications_counter


# ── CRUD Operations ────────────────────────────────────────────────────


def list_auto_applications(user_id: int) -> list[dict[str, Any]]:
    """List all auto-applications for a user."""
    _load_store()
    return [app for app in _auto_applications.values() if app.get("user_id") == user_id]


def get_auto_application(app_id: int) -> dict[str, Any] | None:
    """Get a single auto-application by ID."""
    _load_store()
    return _auto_applications.get(app_id)


def create_auto_application(user_id: int, data: AutoApplicationCreate) -> dict[str, Any]:
    """Create a new auto-application entry."""
    _load_store()
    app_id = _next_id()
    now = datetime.now()
    entry = {
        "id": app_id,
        "user_id": user_id,
        "job_id": None,
        "source": data.source,
        "source_url": data.source_url,
        "company": data.company,
        "job_title": data.job_title,
        "job_description": data.job_description,
        "company_email": data.company_email,
        "status": "sourced",
        "ats_score": None,
        "tailored_resume_text": None,
        "email_sent_to": None,
        "email_sent_at": None,
        "email_subject": None,
        "interview_date": None,
        "interview_type": None,
        "interview_notes": None,
        "followup_count": 0,
        "last_followup_at": None,
        "next_followup_at": None,
        "notes": data.notes,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
    }
    _auto_applications[app_id] = entry
    _save_store()
    return entry


def update_auto_application(app_id: int, user_id: int, data: AutoApplicationUpdate) -> dict[str, Any] | None:
    """Update an auto-application entry."""
    _load_store()
    entry = _auto_applications.get(app_id)
    if not entry or entry.get("user_id") != user_id:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            entry[key] = value
    entry["updated_at"] = datetime.now().isoformat()
    _auto_applications[app_id] = entry
    _save_store()
    return entry


def delete_auto_application(app_id: int, user_id: int) -> bool:
    """Delete an auto-application entry."""
    _load_store()
    entry = _auto_applications.get(app_id)
    if not entry or entry.get("user_id") != user_id:
        return False
    del _auto_applications[app_id]
    _save_store()
    return True


def get_dashboard_stats(user_id: int) -> dict[str, Any]:
    """Get dashboard statistics for auto-apply."""
    _load_store()
    apps = [a for a in _auto_applications.values() if a.get("user_id") == user_id]
    now = datetime.now()

    total_sourced = len(apps)
    total_ai_optimized = sum(1 for a in apps if a.get("tailored_resume_text"))
    total_emailed = sum(1 for a in apps if a.get("email_sent_at"))
    total_interviews = sum(1 for a in apps if a.get("interview_date"))
    total_rejected = sum(1 for a in apps if a.get("status") == "rejected")
    total_accepted = sum(1 for a in apps if a.get("status") == "accepted")

    # Upcoming interviews (next 7 days)
    upcoming_interviews = []
    for a in apps:
        interview_date = a.get("interview_date")
        if interview_date:
            try:
                dt = datetime.fromisoformat(interview_date) if isinstance(interview_date, str) else interview_date
                if now <= dt <= now + timedelta(days=7):
                    upcoming_interviews.append({
                        "id": a["id"],
                        "company": a["company"],
                        "job_title": a["job_title"],
                        "interview_date": dt.isoformat(),
                        "interview_type": a.get("interview_type", "TBD"),
                    })
            except (ValueError, TypeError):
                pass

    # Pending follow-ups (next_followup_at is due or within 2 days)
    pending_followups = sum(
        1 for a in apps
        if a.get("next_followup_at") and not a.get("interview_date")
        and a.get("status") not in ("rejected", "accepted")
    )

    return {
        "total_sourced": total_sourced,
        "total_ai_optimized": total_ai_optimized,
        "total_emailed": total_emailed,
        "total_interviews": total_interviews,
        "total_rejected": total_rejected,
        "total_accepted": total_accepted,
        "pending_followups": pending_followups,
        "upcoming_interviews": upcoming_interviews,
    }


# ── Pipeline Steps ─────────────────────────────────────────────────────


def run_scrape(source: str, query: str, location: str | None = None, max_results: int = 10) -> list[ScrapedJobItem]:
    """
    Step 1: Scrape jobs from a source and create auto-application entries.
    This just scrapes — use import_scraped_jobs to save them.
    """
    return scrape_jobs(source, query, location, max_results)


def import_scraped_jobs(user_id: int, jobs: list[ScrapedJobItem], source: str) -> list[dict[str, Any]]:
    """Save scraped jobs as auto-application entries."""
    created = []
    for job in jobs:
        entry = create_auto_application(
            user_id=user_id,
            data=AutoApplicationCreate(
                source=source,
                source_url=job.url,
                company=job.company,
                job_title=job.title,
                job_description=job.description,
                notes=f"Sourced from {source}",
            ),
        )
        created.append(entry)
    return created


def run_tailor_resume(app_id: int, user_id: int, resume_json: str = "") -> dict[str, Any]:
    """
    Step 2: Tailor resume using AI for a specific application.
    Returns the tailored resume parts and updates the application entry.
    """
    entry = _auto_applications.get(app_id)
    if not entry or entry.get("user_id") != user_id:
        return {"success": False, "message": "Application not found"}

    if not resume_json:
        resume_json = json.dumps({
            "name": "Default Template",
            "skills": "Python, TypeScript, React, FastAPI, PostgreSQL, Docker, AWS, Git",
            "experience": "Senior full-stack developer with 5+ years experience...",
            "education": "B.S. Computer Science",
        })

    result = tailor_resume(
        template_json=resume_json,
        job_title=entry["job_title"],
        company=entry["company"],
        job_description=entry.get("job_description", ""),
    )

    full_resume = build_full_resume_text(
        tailored_parts=result,
        full_name=f"User #{user_id}",
        email=settings.SMTP_FROM_EMAIL,
    )

    entry["tailored_resume_text"] = full_resume
    entry["ats_score"] = result.get("ats_score_estimate", 65)
    entry["status"] = "ai_optimized"
    entry["updated_at"] = datetime.now().isoformat()
    _auto_applications[app_id] = entry
    _save_store()

    return {
        "success": True,
        "message": "Resume tailored successfully",
        "ats_score": entry["ats_score"],
        "professional_summary": result.get("professional_summary", ""),
        "missing_keywords": result.get("missing_keywords", []),
    }


def run_send_application(
    app_id: int,
    user_id: int,
    hr_email: str | None = None,
) -> dict[str, Any]:
    """
    Step 3: Send the application email to the company HR.
    """
    entry = _auto_applications.get(app_id)
    if not entry or entry.get("user_id") != user_id:
        return {"success": False, "message": "Application not found"}

    to_email = hr_email or entry.get("company_email") or f"careers@{entry['company'].lower().replace(' ', '')}.com"
    if not to_email:
        return {"success": False, "message": "No HR email address available"}

    resume_text = entry.get("tailored_resume_text", "Resume not yet tailored. Run AI optimize first.")

    # Generate cover letter
    cover_letter = generate_cover_letter(
        full_name=f"User #{user_id}",
        job_title=entry["job_title"],
        company=entry["company"],
        job_description=entry.get("job_description", ""),
    )

    sent = send_application_email(
        to_email=to_email,
        to_name="Hiring Team",
        job_title=entry["job_title"],
        company=entry["company"],
        applicant_name=f"User #{user_id}",
        resume_text=resume_text,
        cover_letter_text=cover_letter,
    )

    if sent:
        entry["email_sent_to"] = to_email
        entry["email_sent_at"] = datetime.now().isoformat()
        entry["email_subject"] = f"Application for {entry['job_title']} — User #{user_id}"
        entry["status"] = "emailed"
        entry["next_followup_at"] = (datetime.now() + timedelta(days=7)).isoformat()
        entry["updated_at"] = datetime.now().isoformat()
        _auto_applications[app_id] = entry
        _save_store()

        # Notify n8n
        notify_application_updated(
            user_id=user_id,
            user_email=settings.SMTP_FROM_EMAIL,
            application_id=app_id,
            job_id=0,
            company=entry["company"],
            job_title=entry["job_title"],
            previous_status="ai_optimized",
            new_status="emailed",
            applied_date=datetime.now().strftime("%Y-%m-%d"),
        )

        return {"success": True, "message": f"Application sent to {to_email}"}
    else:
        return {"success": False, "message": "Failed to send email. Check SMTP settings."}


def run_full_auto_apply(
    user_id: int,
    source: str,
    query: str,
    location: str | None = None,
    max_results: int = 3,
    resume_json: str = "",
) -> list[dict[str, Any]]:
    """
    Run the complete auto-apply pipeline for a search query.
    1. Scrape jobs
    2. Save as auto-applications
    3. Tailor resume for each
    4. Send application emails
    """
    logger.info("Running full auto-apply: source=%s, query=%s", source, query)

    # Step 1 + 2: Scrape and save
    scraped = run_scrape(source, query, location, max_results)
    created = import_scraped_jobs(user_id, scraped, source)

    results = []
    for entry in created:
        app_id = entry["id"]
        # Step 3: Tailor resume
        tailor_result = run_tailor_resume(app_id, user_id, resume_json)
        if not tailor_result["success"]:
            results.append({"id": app_id, "company": entry["company"], "status": "tailor_failed"})
            continue

        # Step 4: Send email
        send_result = run_send_application(app_id, user_id)
        results.append({
            "id": app_id,
            "company": entry["company"],
            "job_title": entry["job_title"],
            "ats_score": tailor_result.get("ats_score"),
            "email_sent": send_result.get("success", False),
            "email_to": send_result.get("message", ""),
        })

    return results


def schedule_followup(app_id: int, user_id: int) -> dict[str, Any]:
    """
    Send a follow-up email for an application that hasn't heard back.
    Updates followup_count and schedules the next follow-up.
    """
    entry = _auto_applications.get(app_id)
    if not entry or entry.get("user_id") != user_id:
        return {"success": False, "message": "Application not found"}

    to_email = entry.get("email_sent_to")
    if not to_email:
        return {"success": False, "message": "No email to send follow-up to"}

    if entry.get("status") in ("rejected", "accepted"):
        return {"success": False, "message": f"Application already {entry['status']}"}

    sent = send_followup_email(
        to_email=to_email,
        to_name="Hiring Team",
        job_title=entry["job_title"],
        company=entry["company"],
        applicant_name=f"User #{user_id}",
    )

    if sent:
        followup_count = entry.get("followup_count", 0) + 1
        entry["followup_count"] = followup_count
        entry["last_followup_at"] = datetime.now().isoformat()
        # Schedule next follow-up further out (increasing intervals)
        next_days = 7 * min(followup_count + 1, 4)
        entry["next_followup_at"] = (datetime.now() + timedelta(days=next_days)).isoformat()
        if followup_count >= 1:
            entry["status"] = "followup_sent"
        entry["updated_at"] = datetime.now().isoformat()
        _auto_applications[app_id] = entry
        _save_store()
        return {"success": True, "message": f"Follow-up #{followup_count} sent to {to_email}"}
    else:
        return {"success": False, "message": "Failed to send follow-up email"}


def record_interview(
    app_id: int,
    user_id: int,
    interview_date: str,
    interview_type: str = "video",
) -> dict[str, Any]:
    """
    Record an interview date for an application.
    Updates status to interview_scheduled.
    """
    entry = _auto_applications.get(app_id)
    if not entry or entry.get("user_id") != user_id:
        return {"success": False, "message": "Application not found"}

    try:
        dt = datetime.fromisoformat(interview_date)
    except (ValueError, TypeError):
        dt = datetime.now() + timedelta(days=3)

    entry["interview_date"] = dt.isoformat()
    entry["interview_type"] = interview_type
    entry["status"] = "interview_scheduled"
    entry["updated_at"] = datetime.now().isoformat()
    _auto_applications[app_id] = entry
    _save_store()

    # Schedule follow-up after interview
    entry["next_followup_at"] = (dt + timedelta(days=settings.AUTO_APPLY_INTERVIEW_FOLLOWUP_DAYS)).isoformat()

    return {
        "success": True,
        "message": f"Interview recorded for {entry['company']} on {interview_date}",
        "entry": entry,
    }
