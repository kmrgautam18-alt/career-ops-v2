"""
Notification Preferences — Per-user channel and event type configuration.

Database model for user notification preferences.
Allows users to control which events trigger which channels.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, Session

from backend.app.database.base import Base

# Event types that can trigger notifications
EVENT_TYPES = [
    "application.created",
    "application.updated",
    "application.deleted",
    "interview.scheduled",
    "interview.reminder",
    "followup.sent",
    "ai.complete",
    "digest.daily",
    "digest.weekly",
    "job.found",
    "system.alert",
]

# Available notification channels
NOTIFICATION_CHANNELS = ["email", "telegram", "slack", "push", "in_app"]


class NotificationPreference(Base):
    """User notification preferences for each event type and channel."""

    __tablename__ = "notification_preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    channel: Mapped[str] = mapped_column(String(50), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


def get_default_preferences(user_id: int) -> dict[str, dict[str, bool]]:
    """Get default notification preferences for a new user."""
    # Default: all channels enabled for important events
    defaults = {}
    for event in EVENT_TYPES:
        defaults[event] = {}
        for channel in NOTIFICATION_CHANNELS:
            if event in ("digest.daily", "digest.weekly") and channel in ("slack", "push"):
                defaults[event][channel] = False  # Off by default for non-critical
            else:
                defaults[event][channel] = True
    return defaults


def get_preferences(db: Session, user_id: int) -> dict[str, dict[str, bool]]:
    """Load user preferences from DB or return defaults."""
    prefs = (
        db.query(NotificationPreference)
        .filter(NotificationPreference.user_id == user_id)
        .all()
    )

    if not prefs:
        return get_default_preferences(user_id)

    result = get_default_preferences(user_id)
    for p in prefs:
        if p.event_type in result and p.channel in result[p.event_type]:
            result[p.event_type][p.channel] = p.enabled
    return result


def set_preference(
    db: Session,
    user_id: int,
    event_type: str,
    channel: str,
    enabled: bool,
) -> NotificationPreference:
    """Set a notification preference."""
    pref = (
        db.query(NotificationPreference)
        .filter(
            NotificationPreference.user_id == user_id,
            NotificationPreference.event_type == event_type,
            NotificationPreference.channel == channel,
        )
        .first()
    )

    if pref:
        pref.enabled = enabled
    else:
        pref = NotificationPreference(
            user_id=user_id,
            event_type=event_type,
            channel=channel,
            enabled=enabled,
        )
        db.add(pref)

    db.commit()
    return pref
