"""
Notification Preferences API endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.models.notification_preference import (
    EVENT_TYPES,
    NOTIFICATION_CHANNELS,
    get_preferences,
    set_preference,
)
from backend.app.schemas.common_schema import ApiResponse
from backend.app.security.dependencies import get_current_active_user

router = APIRouter(
    prefix="/notifications/preferences",
    tags=["Notification Preferences"],
)


@router.get("/events")
def list_event_types():
    """List all available notification event types."""
    return ApiResponse(
        success=True,
        message="Event types retrieved.",
        data={"event_types": EVENT_TYPES, "channels": NOTIFICATION_CHANNELS},
    )


@router.get("/")
def get_my_preferences(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get notification preferences for the current user."""
    prefs = get_preferences(db, current_user.id)
    return ApiResponse(success=True, message="Preferences retrieved.", data=prefs)


@router.put("/{event_type}/{channel}")
def update_preference(
    event_type: str,
    channel: str,
    enabled: bool = True,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Update a specific notification preference."""
    if event_type not in EVENT_TYPES:
        return ApiResponse(success=False, message=f"Invalid event type: {event_type}.", data=None)
    if channel not in NOTIFICATION_CHANNELS:
        return ApiResponse(success=False, message=f"Invalid channel: {channel}.", data=None)

    set_preference(db, current_user.id, event_type, channel, enabled)
    return ApiResponse(
        success=True,
        message=f"Preference updated: {event_type} → {channel} = {'enabled' if enabled else 'disabled'}",
        data=None,
    )


@router.put("/all")
def update_all_preferences(
    enabled: bool = True,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Enable or disable all notification preferences."""
    for event_type in EVENT_TYPES:
        for channel in NOTIFICATION_CHANNELS:
            set_preference(db, current_user.id, event_type, channel, enabled)
    return ApiResponse(
        success=True,
        message=f"All notifications {'enabled' if enabled else 'disabled'}.",
        data=None,
    )
