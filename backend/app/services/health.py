"""
Health Check Endpoints for Career-Ops.
Provides /health, /ready, /live for Kubernetes, load balancers, and monitoring.
"""

from __future__ import annotations

import logging
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app import __version__
from backend.app.database.dependencies import get_db

logger = logging.getLogger(__name__)

health_router = APIRouter(tags=["Health"])

# ── Service Status ─────────────────────────────────────────────────────


def _check_database(db: Session) -> dict:
    """Check database connectivity."""
    try:
        start = datetime.now()
        db.execute(text("SELECT 1"))
        elapsed = (datetime.now() - start).total_seconds()
        return {"status": "healthy", "latency_ms": round(elapsed * 1000, 2), "type": str(db.bind.name) if db.bind else "unknown"}
    except Exception as e:
        logger.error("Database health check failed: %s", e)
        return {"status": "unhealthy", "error": str(e)}


def _check_disk() -> dict:
    """Check disk space."""
    import shutil

    try:
        usage = shutil.disk_usage("/")
        percent_free = (usage.free / usage.total) * 100
        return {
            "status": "healthy" if percent_free > 10 else "warning",
            "free_gb": round(usage.free / (1024**3), 2),
            "total_gb": round(usage.total / (1024**3), 2),
            "percent_free": round(percent_free, 1),
        }
    except Exception as e:
        return {"status": "unknown", "error": str(e)}


def _check_llm() -> dict:
    """Check LLM/AI provider connectivity."""
    from backend.app.core.config import settings

    if settings.LLM_API_KEY:
        try:
            import google.generativeai as genai

            genai.configure(api_key=settings.LLM_API_KEY)
            # Lightweight model list check
            models = genai.list_models()
            available = any(m.name == f"models/{settings.LLM_MODEL}" for m in models)
            return {
                "status": "healthy" if available else "warning",
                "provider": settings.LLM_PROVIDER,
                "model": settings.LLM_MODEL,
                "available": available,
            }
        except Exception as e:
            return {"status": "degraded", "provider": settings.LLM_PROVIDER, "error": str(e)}
    else:
        return {"status": "disabled", "provider": "none", "message": "No LLM_API_KEY configured"}


# ── Endpoints ──────────────────────────────────────────────────────────


@health_router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Comprehensive health check for monitoring and orchestration."""
    db_status = _check_database(db)
    disk_status = _check_disk()
    llm_status = _check_llm()

    all_healthy = all(s["status"] == "healthy" for s in [db_status, disk_status] if s["status"] != "disabled")

    return {
        "application": "Career-Ops v2",
        "version": __version__,
        "timestamp": datetime.now().isoformat(),
        "status": "healthy" if all_healthy else "degraded",
        "checks": {
            "database": db_status,
            "disk": disk_status,
            "llm": llm_status,
        },
    }


@health_router.get("/ready")
def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness probe — indicates if the app is ready to serve traffic.
    Used by Kubernetes readinessProbe and load balancers.
    """
    db_status = _check_database(db)

    if db_status["status"] == "healthy":
        return {
            "status": "ready",
            "timestamp": datetime.now().isoformat(),
        }
    else:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=503,
            detail={
                "status": "not_ready",
                "reason": "Database unavailable",
                "database": db_status,
            },
        )


@health_router.get("/live")
def liveness_check():
    """
    Liveness probe — indicates if the app process is alive.
    Used by Kubernetes livenessProbe.
    """
    return {
        "status": "alive",
        "timestamp": datetime.now().isoformat(),
    }
