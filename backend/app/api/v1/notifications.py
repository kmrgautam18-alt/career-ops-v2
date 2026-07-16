"""
Module 15 — Notifications (Email, SMS, Push, Slack, Discord, Telegram, In-App)
"""
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query

from backend.app.schemas.notification_schema import (
    NotificationCreate,
    NotificationPreferences,
)
from backend.app.security.dependencies import get_current_active_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])

_notifications_db: dict[int, list[dict]] = {}

@router.get("/")
def list_notifications(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    unread_only: bool = False,
    current_user=Depends(get_current_active_user),
):
    user_notifications = _notifications_db.get(current_user.id, [])
    if unread_only:
        user_notifications = [n for n in user_notifications if not n["is_read"]]
    start = (page - 1) * size
    paginated = user_notifications[start:start + size]
    unread_count = sum(1 for n in user_notifications if not n["is_read"])
    return {
        "success": True,
        "data": paginated,
        "pagination": {"page": page, "size": size, "total": len(user_notifications), "unread": unread_count},
    }


@router.post("/")
def create_notification(
    data: NotificationCreate,
    current_user=Depends(get_current_active_user),
):
    if current_user.id not in _notifications_db:
        _notifications_db[current_user.id] = []
    notif = {
        "id": len(_notifications_db[current_user.id]) + 1,
        "user_id": current_user.id,
        "type": data.type,
        "title": data.title,
        "message": data.message,
        "channel": data.channel,
        "is_read": False,
        "created_at": datetime.now(UTC).isoformat(),
    }
    _notifications_db[current_user.id].insert(0, notif)
    return {"success": True, "data": notif}


@router.patch("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    current_user=Depends(get_current_active_user),
):
    user_notifications = _notifications_db.get(current_user.id, [])
    for n in user_notifications:
        if n["id"] == notification_id:
            n["is_read"] = True
            return {"success": True, "data": n}
    return {"success": False, "message": "Notification not found."}


@router.post("/mark-all-read")
def mark_all_read(
    current_user=Depends(get_current_active_user),
):
    user_notifications = _notifications_db.get(current_user.id, [])
    for n in user_notifications:
        n["is_read"] = True
    return {"success": True, "message": "All notifications marked as read."}


@router.get("/preferences")
def get_preferences(
    current_user=Depends(get_current_active_user),
):
    return {"success": True, "data": NotificationPreferences().model_dump()}


@router.put("/preferences")
def update_preferences(
    prefs: NotificationPreferences,
    current_user=Depends(get_current_active_user),
):
    return {"success": True, "data": prefs.model_dump()}
