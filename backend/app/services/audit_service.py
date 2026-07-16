"""
Audit Logging Service — Tracks all user actions for compliance and security.
Every create/update/delete operation is logged with actor, action, resource, timestamp.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from fastapi import Request
from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal
from backend.app.models.audit_log import AuditLog
from backend.app.models.user import User

logger = logging.getLogger(__name__)


def log_action(
    db: Session,
    user_id: int,
    action: str,
    resource: str | None = None,
    resource_id: int | None = None,
    details: dict[str, Any] | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> AuditLog:
    """Create an audit log entry."""
    entry = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        resource_id=resource_id,
        details=json.dumps(details) if details else None,
        ip_address=ip_address,
        user_agent=user_agent[:500] if user_agent else None,
    )
    db.add(entry)
    db.commit()
    return entry


def get_audit_logs(
    db: Session,
    user_id: int | None = None,
    action: str | None = None,
    resource: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[AuditLog]:
    """Retrieve audit logs with optional filters."""
    query = db.query(AuditLog)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if action:
        query = query.filter(AuditLog.action == action)
    if resource:
        query = query.filter(AuditLog.resource == resource)
    return query.order_by(AuditLog.created_at.desc()).limit(limit).offset(offset).all()


async def log_request_action(
    request: Request,
    user: User,
    action: str,
    resource: str | None = None,
    resource_id: int | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    """Convenience: extract IP/User-Agent from request and log."""
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent", None)
    try:
        db = SessionLocal()
        log_action(
            db=db,
            user_id=user.id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details,
            ip_address=ip,
            user_agent=ua,
        )
    except Exception as e:
        logger.warning(f"Failed to write audit log: {e}")
