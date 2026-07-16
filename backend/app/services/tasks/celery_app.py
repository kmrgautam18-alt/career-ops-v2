"""
Celery Application Configuration.
Provides async background task processing for:
- AI operations (ATS scoring, resume optimization, interview generation)
- Bulk email sending (application + follow-up campaigns)
- Data cleanup (temp file removal, cache warming)
- Scheduled health checks
"""

from __future__ import annotations

import logging
from typing import Any

from celery import Celery
from celery.schedules import crontab

from backend.app.core.config import settings

logger = logging.getLogger(__name__)

# ── Celery App ──────────────────────────────────────────────────────────

celery_app = Celery(
    "careerops",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "backend.app.services.tasks.ai_tasks",
        "backend.app.services.tasks.email_tasks",
        "backend.app.services.tasks.cleanup_tasks",
    ],
)

# ── Configuration ──────────────────────────────────────────────────────

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=5 * 60,  # 5 minutes max per task
    task_soft_time_limit=4 * 60,  # 4 minute soft limit
    worker_max_tasks_per_child=100,
    worker_concurrency=4,
    result_expires=3600,  # Results expire after 1 hour
)

# ── Periodic Tasks (Celery Beat) ──────────────────────────────────────

celery_app.conf.beat_schedule = {
    # Daily cleanup: remove old temp files, expired cache
    "daily-cleanup": {
        "task": "backend.app.services.tasks.cleanup_tasks.cleanup_temp_files",
        "schedule": crontab(hour=3, minute=0),  # 3 AM daily
    },
    # Hourly: warm cache for popular dashboard stats
    "hourly-cache-warm": {
        "task": "backend.app.services.tasks.cleanup_tasks.warm_popular_caches",
        "schedule": crontab(minute="0"),  # Every hour
    },
    # Weekly: database maintenance
    "weekly-db-maintenance": {
        "task": "backend.app.services.tasks.cleanup_tasks.database_maintenance",
        "schedule": crontab(hour=2, minute=30, day_of_week="sunday"),
    },
}


# ── Task Base ────────────────────────────────────────────────────────────


class TaskBase:
    """Base class with shared utilities for all tasks."""

    @staticmethod
    def get_db_session():
        """Get a fresh DB session for task execution."""
        from backend.app.database.session import SessionLocal

        return SessionLocal()
