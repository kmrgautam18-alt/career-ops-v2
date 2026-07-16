"""Audit Log API endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.schemas.common_schema import ApiResponse
from backend.app.security.dependencies import get_current_active_user, get_current_admin_user
from backend.app.services.audit_service import get_audit_logs

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


@router.get("/")
def list_audit_logs(
    action: str | None = Query(None),
    resource: str | None = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get audit logs (users see their own, admins see all)."""
    user_id = None if current_user.role == "ADMIN" else current_user.id
    logs = get_audit_logs(
        db=db,
        user_id=user_id,
        action=action,
        resource=resource,
        limit=limit,
        offset=offset,
    )
    return ApiResponse(
        success=True,
        message="Audit logs retrieved.",
        data=[
            {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "resource": log.resource,
                "resource_id": log.resource_id,
                "details": log.details,
                "ip_address": log.ip_address,
                "created_at": log.created_at.isoformat() if log.created_at else None,
            }
            for log in logs
        ],
    )
