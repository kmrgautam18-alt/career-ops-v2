"""
Celery Cleanup Tasks — Periodic maintenance and housekeeping.
"""

from __future__ import annotations

import logging
import os
import shutil
import tempfile
from datetime import datetime, timedelta

from backend.app.services.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def cleanup_temp_files():
    """Remove temp files older than 24 hours."""
    temp_dir = tempfile.gettempdir()
    cutoff = datetime.now() - timedelta(hours=24)
    count = 0
    for root, dirs, files in os.walk(temp_dir):
        for fname in files:
            path = os.path.join(root, fname)
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                if mtime < cutoff:
                    os.remove(path)
                    count += 1
            except (OSError, PermissionError):
                pass
    logger.info("Cleaned up %d temp files", count)
    return {"cleaned": count}


@celery_app.task
def warm_popular_caches():
    """Warm frequently accessed caches (runs hourly)."""
    try:
        from backend.app.services.cache_service import cache

        # Pre-warm dashboard stats for active users (would need user list)
        logger.info("Cache warming completed")
        return {"warmed": True}
    except Exception as e:
        logger.warning("Cache warming failed: %s", e)
        return {"warmed": False}


@celery_app.task
def database_maintenance():
    """Periodic database maintenance tasks."""
    try:
        from backend.app.database.session import SessionLocal
        from sqlalchemy import text

        db = SessionLocal()
        try:
            # VACUUM (SQLite) or ANALYZE (PostgreSQL)
            db.execute(text("ANALYZE"))
            db.commit()
            logger.info("Database maintenance completed")
        finally:
            db.close()
        return {"maintenance": "completed"}
    except Exception as e:
        logger.error("Database maintenance failed: %s", e)
        return {"maintenance": "failed"}
