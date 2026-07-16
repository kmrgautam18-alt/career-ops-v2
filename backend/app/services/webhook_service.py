"""
Webhook Service for n8n Integration
Sends asynchronous HTTP POST requests to n8n when key events occur.
"""

import logging
from typing import Any

import requests

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


def _send_webhook(event: str, payload: dict[str, Any]) -> bool:
    """
    Send a webhook event to n8n.

    Args:
        event: The webhook event name (becomes the URL path).
        payload: JSON-serializable data to send.

    Returns:
        True if the webhook was sent successfully, False otherwise.
    """
    if not settings.N8N_ENABLED:
        logger.debug("n8n webhook disabled — set N8N_ENABLED=true to enable")
        return False

    url = f"{settings.N8N_WEBHOOK_BASE_URL.rstrip('/')}/webhook/{event}"
    try:
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
        logger.info("n8n webhook sent: event=%s, status=%s", event, resp.status_code)
        return True
    except requests.RequestException as exc:
        logger.warning("n8n webhook failed: event=%s, error=%s", event, exc)
        return False


# ── Public API ──────────────────────────────────────────────────────────


def notify_application_created(
    user_id: int,
    user_email: str,
    application_id: int,
    job_id: int,
    company: str | None,
    job_title: str | None,
    status: str,
    applied_date: str,
):
    """Notify n8n that a new application was created."""
    _send_webhook("careerops-application-created", {
        "event": "application.created",
        "user_id": user_id,
        "user_email": user_email,
        "application_id": application_id,
        "job_id": job_id,
        "company": company or "Unknown",
        "job_title": job_title or "Unknown",
        "status": status,
        "applied_date": applied_date,
    })


def notify_application_updated(
    user_id: int,
    user_email: str,
    application_id: int,
    job_id: int,
    company: str | None,
    job_title: str | None,
    previous_status: str,
    new_status: str,
    applied_date: str,
):
    """Notify n8n that an application status changed."""
    _send_webhook("careerops-application-status", {
        "event": "application.updated",
        "user_id": user_id,
        "user_email": user_email,
        "application_id": application_id,
        "job_id": job_id,
        "company": company or "Unknown",
        "job_title": job_title or "Unknown",
        "previous_status": previous_status,
        "status": new_status,
        "applied_date": applied_date,
    })


def notify_application_deleted(
    user_id: int,
    user_email: str,
    application_id: int,
    job_id: int,
    company: str | None,
    job_title: str | None,
    previous_status: str,
):
    """Notify n8n that an application was deleted."""
    _send_webhook("careerops-application-deleted", {
        "event": "application.deleted",
        "user_id": user_id,
        "user_email": user_email,
        "application_id": application_id,
        "job_id": job_id,
        "company": company or "Unknown",
        "job_title": job_title or "Unknown",
        "previous_status": previous_status,
    })
