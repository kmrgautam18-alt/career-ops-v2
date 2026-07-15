from datetime import datetime
from pydantic import BaseModel


class CalendarEventCreate(BaseModel):
    title: str
    description: str = ""
    event_type: str  # interview, deadline, goal, reminder, learning
    start_time: datetime
    end_time: datetime | None = None
    all_day: bool = False
    related_id: int | None = None  # job_id, application_id, etc.


class CalendarEventResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    event_type: str
    start_time: datetime
    end_time: datetime | None
    all_day: bool
    related_id: int | None
    created_at: datetime

    model_config = {"from_attributes": True}


class CalendarEventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    all_day: bool | None = None


class CalendarSyncResponse(BaseModel):
    provider: str
    last_synced: datetime | None
    events_count: int
