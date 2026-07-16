"""
Pydantic schemas for the Auto Job Application Engine.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# ── Resume Template Schemas ───────────────────────────────────────────


class ResumeTemplateCreate(BaseModel):
    name: str = "Default"
    template_json: str = ""
    work_experience: str | None = None
    education: str | None = None
    skills: str | None = None
    certifications: str | None = None
    projects: str | None = None
    is_default: bool = False


class ResumeTemplateUpdate(BaseModel):
    name: str | None = None
    template_json: str | None = None
    work_experience: str | None = None
    education: str | None = None
    skills: str | None = None
    certifications: str | None = None
    projects: str | None = None
    is_default: bool | None = None


class ResumeTemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    template_json: str
    work_experience: str | None
    education: str | None
    skills: str | None
    certifications: str | None
    projects: str | None
    is_default: bool
    created_at: datetime
    updated_at: datetime


# ── Auto Application Schemas ──────────────────────────────────────────


class AutoApplicationCreate(BaseModel):
    """Create an auto-application entry (sourced job)."""

    source: str = Field(default="manual", description="linkedin, indeed, company_career, manual")
    source_url: str | None = None
    company: str
    job_title: str
    job_description: str | None = None
    company_email: str | None = None
    notes: str | None = None


class AutoApplicationUpdate(BaseModel):
    """Update an auto-application (status, interview, notes)."""

    status: str | None = None
    company_email: str | None = None
    interview_date: datetime | None = None
    interview_type: str | None = None
    interview_notes: str | None = None
    notes: str | None = None


class AutoApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    job_id: int | None
    source: str
    source_url: str | None
    company: str
    job_title: str
    job_description: str | None
    company_email: str | None
    status: str
    ats_score: int | None
    tailored_resume_text: str | None
    email_sent_to: str | None
    email_sent_at: datetime | None
    email_subject: str | None
    interview_date: datetime | None
    interview_type: str | None
    interview_notes: str | None
    followup_count: int
    last_followup_at: datetime | None
    next_followup_at: datetime | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


# ── Action Request/Response Schemas ────────────────────────────────────


class AutoApplyTriggerRequest(BaseModel):
    """Trigger the full auto-apply pipeline for a specific entry."""

    application_id: int
    resume_template_id: int | None = None


class AutoApplyTriggerResponse(BaseModel):
    success: bool
    message: str
    data: dict[str, Any] | None = None


class ResumeBuildRequest(BaseModel):
    """Request to build a tailored resume for a job."""

    application_id: int
    resume_template_id: int | None = None


class ResumeBuildResponse(BaseModel):
    success: bool
    message: str
    ats_score: int | None = None
    tailored_resume: str | None = None


class ScrapeJobRequest(BaseModel):
    """Request to scrape jobs from a source."""

    source: str = Field(description="linkedin, indeed, company_career")
    query: str = Field(description="Job search query (e.g. 'Python Developer')")
    location: str | None = None
    max_results: int = 10


class ScrapedJobItem(BaseModel):
    company: str
    title: str
    url: str
    description: str | None = None
    location: str | None = None


class ScrapeJobResponse(BaseModel):
    success: bool
    source: str
    count: int
    jobs: list[ScrapedJobItem]


class DashboardStats(BaseModel):
    total_sourced: int = 0
    total_ai_optimized: int = 0
    total_emailed: int = 0
    total_interviews: int = 0
    total_rejected: int = 0
    total_accepted: int = 0
    pending_followups: int = 0
    upcoming_interviews: list[dict[str, Any]] = []
