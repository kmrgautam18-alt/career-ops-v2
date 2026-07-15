from datetime import datetime
from pydantic import BaseModel


class NotificationCreate(BaseModel):
    type: str  # email, sms, push, slack, discord, telegram, in_app
    title: str
    message: str
    channel: str = "in_app"


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: str
    title: str
    message: str
    channel: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationPreferences(BaseModel):
    email: bool = True
    sms: bool = False
    push: bool = True
    slack: bool = False
    discord: bool = False
    telegram: bool = False
    in_app: bool = True
