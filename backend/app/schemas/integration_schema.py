from datetime import datetime
from pydantic import BaseModel


class IntegrationCreate(BaseModel):
    provider: str  # linkedin, github, google, gmail, slack, etc.
    access_token: str = ""
    refresh_token: str = ""
    token_expiry: datetime | None = None


class IntegrationResponse(BaseModel):
    id: int
    user_id: int
    provider: str
    is_connected: bool
    connected_at: datetime | None
    last_synced: datetime | None

    model_config = {"from_attributes": True}


class OAuthUrlResponse(BaseModel):
    url: str
    provider: str
    state: str
