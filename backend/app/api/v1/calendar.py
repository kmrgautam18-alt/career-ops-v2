"""
Module 16 — Calendar (Interview Schedule, Learning, Goals, Reminders, Sync)
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query

from backend.app.schemas.calendar_schema import CalendarEventCreate, CalendarEventResponse, CalendarEventUpdate
from backend.app.security.dependencies import get_current_active_user

router = APIRouter(prefix="/calendar", tags=["Calendar"])

_events_db: dict[int, list[dict]] = {}

@router.get("/events")
def list_events(
    start_date: str = "",
    end_date: str = "",
    event_type: str = "",
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
    current_user=Depends(get_current_active_user),
):
    events = _events_db.get(current_user.id, [])
    if event_type:
        events = [e for e in events if e["event_type"] == event_type]
    if start_date:
        events = [e for e in events if e["start_time"] >= start_date]
    if end_date:
        events = [e for e in events if e["start_time"] <= end_date]
    start = (page - 1) * size
    return {
        "success": True,
        "data": events[start:start + size],
        "pagination": {"page": page, "size": size, "total": len(events)},
    }


@router.post("/events")
def create_event(
    data: CalendarEventCreate,
    current_user=Depends(get_current_active_user),
):
    if current_user.id not in _events_db:
        _events_db[current_user.id] = []
    event = {
        "id": len(_events_db[current_user.id]) + 1,
        "user_id": current_user.id,
        "title": data.title,
        "description": data.description,
        "event_type": data.event_type,
        "start_time": data.start_time.isoformat() if hasattr(data.start_time, 'isoformat') else str(data.start_time),
        "end_time": data.end_time.isoformat() if data.end_time and hasattr(data.end_time, 'isoformat') else str(data.end_time) if data.end_time else None,
        "all_day": data.all_day,
        "related_id": data.related_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _events_db[current_user.id].append(event)
    return {"success": True, "data": event}


@router.patch("/events/{event_id}")
def update_event(
    event_id: int,
    data: CalendarEventUpdate,
    current_user=Depends(get_current_active_user),
):
    events = _events_db.get(current_user.id, [])
    for e in events:
        if e["id"] == event_id:
            if data.title is not None: e["title"] = data.title
            if data.description is not None: e["description"] = data.description
            if data.start_time is not None: e["start_time"] = data.start_time.isoformat() if hasattr(data.start_time, 'isoformat') else str(data.start_time)
            if data.end_time is not None: e["end_time"] = data.end_time.isoformat() if hasattr(data.end_time, 'isoformat') else str(data.end_time)
            if data.all_day is not None: e["all_day"] = data.all_day
            return {"success": True, "data": e}
    return {"success": False, "message": "Event not found."}


@router.delete("/events/{event_id}")
def delete_event(
    event_id: int,
    current_user=Depends(get_current_active_user),
):
    events = _events_db.get(current_user.id, [])
    _events_db[current_user.id] = [e for e in events if e["id"] != event_id]
    return {"success": True, "message": "Event deleted."}


@router.get("/upcoming")
def get_upcoming_events(
    days: int = 7,
    current_user=Depends(get_current_active_user),
):
    events = _events_db.get(current_user.id, [])
    upcoming = [e for e in events if e["start_time"] >= datetime.now(timezone.utc).isoformat()][:10]
    return {"success": True, "data": upcoming}


@router.post("/sync/{provider}")
def sync_calendar(
    provider: str,
    current_user=Depends(get_current_active_user),
):
    return {
        "success": True,
        "data": {"provider": provider, "last_synced": datetime.now(timezone.utc).isoformat(), "events_count": 0},
    }
