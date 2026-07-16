"""
Celery AI Tasks — Background processing for all AI operations.
Prevents blocking the API when running expensive Gemini calls.
"""

from __future__ import annotations

import logging
from typing import Any

from backend.app.services.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=2, default_retry_delay=30)
def async_ats_score(self, resume_text: str, job_description: str) -> dict[str, Any]:
    """Evaluate ATS score in the background."""
    try:
        from backend.app.services.llm_service import ats_evaluate

        result = ats_evaluate(resume_text, job_description)
        logger.info("Async ATS score completed")
        return {"success": True, "data": result}
    except Exception as exc:
        logger.error("Async ATS score failed: %s", exc)
        raise self.retry(exc=exc) from exc


@celery_app.task(bind=True, max_retries=2, default_retry_delay=30)
def async_interview_questions(
    self, job_title: str, company: str, difficulty: str = "medium", count: int = 8
) -> dict[str, Any]:
    """Generate interview questions in the background."""
    try:
        from backend.app.services.llm_service import generate_interview_questions

        questions = generate_interview_questions(job_title, company, difficulty, count)
        logger.info("Async interview questions generated: %d questions", len(questions))
        return {"success": True, "data": questions}
    except Exception as exc:
        logger.error("Async interview questions failed: %s", exc)
        raise self.retry(exc=exc) from exc


@celery_app.task(bind=True, max_retries=2, default_retry_delay=30)
def async_resume_optimize(self, resume_text: str, job_description: str) -> dict[str, Any]:
    """Optimize resume in the background."""
    try:
        from backend.app.services.llm_service import optimize_resume

        result = optimize_resume(resume_text, job_description)
        logger.info("Async resume optimization completed")
        return {"success": True, "data": result}
    except Exception as exc:
        logger.error("Async resume optimization failed: %s", exc)
        raise self.retry(exc=exc) from exc


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def async_job_match(self, profile: str, job_details: str) -> dict[str, Any]:
    """Match a profile against a job description in the background."""
    try:
        from backend.app.services.llm_service import job_match_ai

        result = job_match_ai(profile, job_details)
        logger.info("Async job match completed")
        return {"success": True, "data": result}
    except Exception as exc:
        logger.error("Async job match failed: %s", exc)
        raise self.retry(exc=exc) from exc


@celery_app.task(bind=True, max_retries=2, default_retry_delay=30)
def async_tailor_resume(self, template_json: str, job_title: str, company: str, job_description: str) -> dict[str, Any]:
    """Tailor a resume to a specific job in the background (auto-apply engine)."""
    try:
        from backend.app.services.resume_builder_service import tailor_resume

        result = tailor_resume(template_json, job_title, company, job_description)
        logger.info("Async resume tailoring completed for %s at %s", job_title, company)
        return {"success": True, "data": result}
    except Exception as exc:
        logger.error("Async resume tailoring failed: %s", exc)
        raise self.retry(exc=exc) from exc
