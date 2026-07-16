"""
Data Export Service — GDPR-compliant user data portability.
Exports all user data as JSON or CSV.
"""

from __future__ import annotations

import csv
import io
import logging
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from backend.app.models.application import Application
from backend.app.models.auto_application import AutoApplication, ResumeTemplate
from backend.app.models.job import Job
from backend.app.models.resume import Resume
from backend.app.models.user import User

logger = logging.getLogger(__name__)


def _model_to_dict(obj: Any) -> dict[str, Any]:
    """Convert a SQLAlchemy model instance to a dict, skipping relationships."""
    if obj is None:
        return {}
    result = {}
    for column in obj.__table__.columns:
        value = getattr(obj, column.name)
        if isinstance(value, datetime):
            value = value.isoformat()
        result[column.name] = value
    return result


def export_user_data_json(db: Session, user: User) -> dict[str, Any]:
    """Export all user data as a JSON-serializable dict."""
    user_data = _model_to_dict(user)
    user_data.pop("hashed_password", None)

    jobs = db.query(Job).filter(Job.user_id == user.id).all()
    applications = db.query(Application).filter(Application.user_id == user.id).all()
    resumes = db.query(Resume).filter(Resume.user_id == user.id).all()
    auto_applications = db.query(AutoApplication).filter(AutoApplication.user_id == user.id).all()
    templates = db.query(ResumeTemplate).filter(ResumeTemplate.user_id == user.id).all()

    return {
        "export_date": datetime.utcnow().isoformat(),
        "user": user_data,
        "jobs": [_model_to_dict(j) for j in jobs],
        "applications": [_model_to_dict(a) for a in applications],
        "resumes": [_model_to_dict(r) for r in resumes],
        "auto_applications": [_model_to_dict(aa) for aa in auto_applications],
        "resume_templates": [_model_to_dict(t) for t in templates],
    }


def export_user_data_csv(db: Session, user: User) -> dict[str, str]:
    """Export all user data as CSV strings keyed by table name."""
    result: dict[str, str] = {}

    jobs = db.query(Job).filter(Job.user_id == user.id).all()
    applications = db.query(Application).filter(Application.user_id == user.id).all()
    resumes = db.query(Resume).filter(Resume.user_id == user.id).all()
    auto_applications = db.query(AutoApplication).filter(AutoApplication.user_id == user.id).all()

    # Jobs CSV
    if jobs:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "title", "company", "location", "status", "url", "created_at"])
        for j in jobs:
            writer.writerow([j.id, j.title, j.company, j.location, j.status, j.url, j.created_at])
        result["jobs"] = output.getvalue()

    # Applications CSV
    if applications:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "job_title", "company", "status", "applied_date", "notes", "created_at"])
        for a in applications:
            writer.writerow([a.id, a.job_title, a.company, a.status, a.applied_date, a.notes, a.created_at])
        result["applications"] = output.getvalue()

    # Resumes CSV
    if resumes:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "title", "original_filename", "file_type", "created_at"])
        for r in resumes:
            writer.writerow([r.id, r.title, r.original_filename, r.file_type, r.created_at])
        result["resumes"] = output.getvalue()

    # Auto-Applications CSV
    if auto_applications:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "job_title", "company", "source", "status", "hr_email", "ats_score_before", "ats_score_after", "created_at"])
        for aa in auto_applications:
            writer.writerow([aa.id, aa.job_title, aa.company, aa.source, aa.status, aa.hr_email, aa.ats_score_before, aa.ats_score_after, aa.created_at])
        result["auto_applications"] = output.getvalue()

    return result
