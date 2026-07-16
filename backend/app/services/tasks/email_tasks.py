"""
Celery Email Tasks — Send emails asynchronously to avoid blocking the API.
"""

from __future__ import annotations

import logging
from typing import Any

from backend.app.services.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_application_email_async(
    self,
    to_email: str,
    to_name: str,
    job_title: str,
    company: str,
    applicant_name: str,
    resume_text: str,
    cover_letter_text: str | None = None,
) -> dict[str, Any]:
    """Send a job application email in the background."""
    try:
        from backend.app.services.email_service import send_application_email

        success = send_application_email(
            to_email=to_email,
            to_name=to_name,
            job_title=job_title,
            company=company,
            applicant_name=applicant_name,
            resume_text=resume_text,
            cover_letter_text=cover_letter_text,
        )
        logger.info("Async application email to %s: %s", to_email, "sent" if success else "failed")
        return {"success": success, "to": to_email}
    except Exception as exc:
        logger.error("Async email to %s failed: %s", to_email, exc)
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_followup_email_async(
    self,
    to_email: str,
    to_name: str,
    job_title: str,
    company: str,
    applicant_name: str,
) -> dict[str, Any]:
    """Send a follow-up email in the background."""
    try:
        from backend.app.services.email_service import send_followup_email

        success = send_followup_email(
            to_email=to_email,
            to_name=to_name,
            job_title=job_title,
            company=company,
            applicant_name=applicant_name,
        )
        logger.info("Async follow-up email to %s: %s", to_email, "sent" if success else "failed")
        return {"success": success, "to": to_email}
    except Exception as exc:
        logger.error("Async follow-up to %s failed: %s", to_email, exc)
        raise self.retry(exc=exc)
