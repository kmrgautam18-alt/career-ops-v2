"""
Module 20 — Integrations (LinkedIn, GitHub, Google, Gmail, Slack, Notion, etc.)
"""
from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends

from backend.app.schemas.integration_schema import OAuthUrlResponse
from backend.app.security.dependencies import get_current_active_user

router = APIRouter(prefix="/integrations", tags=["Integrations"])

_PROVIDERS = {
    "linkedin": {"name": "LinkedIn", "icon": "linkedin", "color": "#0A66C2", "scopes": ["profile", "email"]},
    "github": {"name": "GitHub", "icon": "github", "color": "#333", "scopes": ["repo", "user"]},
    "google": {"name": "Google", "icon": "google", "color": "#4285F4", "scopes": ["profile", "email", "drive"]},
    "gmail": {"name": "Gmail", "icon": "mail", "color": "#EA4335", "scopes": ["mail.send", "mail.read"]},
    "outlook": {"name": "Outlook", "icon": "mail", "color": "#0078D4", "scopes": ["mail.send", "calendar"]},
    "slack": {"name": "Slack", "icon": "message-square", "color": "#4A154B", "scopes": ["chat:write", "channels:read"]},
    "discord": {"name": "Discord", "icon": "message-circle", "color": "#5865F2", "scopes": ["bot", "webhook"]},
    "google_drive": {"name": "Google Drive", "icon": "folder", "color": "#34A853", "scopes": ["drive.file"]},
    "dropbox": {"name": "Dropbox", "icon": "folder", "color": "#0061FF", "scopes": ["files.read"]},
    "onedrive": {"name": "OneDrive", "icon": "cloud", "color": "#0078D4", "scopes": ["files.read"]},
    "notion": {"name": "Notion", "icon": "book", "color": "#000", "scopes": ["read", "write"]},
    "google_calendar": {"name": "Google Calendar", "icon": "calendar", "color": "#4285F4", "scopes": ["calendar"]},
}

_integrations_db: dict[int, list[dict]] = {}

@router.get("/providers")
def list_providers(current_user=Depends(get_current_active_user)):
    return {
        "success": True,
        "data": [
            {"id": pid, **p, "is_connected": _is_connected(current_user.id, pid)}
            for pid, p in _PROVIDERS.items()
        ],
    }


@router.get("/")
def list_integrations(current_user=Depends(get_current_active_user)):
    return {
        "success": True,
        "data": _integrations_db.get(current_user.id, []),
    }


@router.post("/{provider}/connect")
def connect_integration(
    provider: str,
    current_user=Depends(get_current_active_user),
):
    if provider not in _PROVIDERS:
        return {"success": False, "message": f"Unknown provider: {provider}"}
    if current_user.id not in _integrations_db:
        _integrations_db[current_user.id] = []
    integration = {
        "id": len(_integrations_db[current_user.id]) + 1,
        "user_id": current_user.id,
        "provider": provider,
        "is_connected": True,
        "connected_at": datetime.now(UTC).isoformat(),
        "last_synced": None,
        "scopes": _PROVIDERS[provider]["scopes"],
    }
    _integrations_db[current_user.id] = [
        i for i in _integrations_db[current_user.id] if i["provider"] != provider
    ]
    _integrations_db[current_user.id].append(integration)
    return {"success": True, "data": integration}


@router.post("/{provider}/disconnect")
def disconnect_integration(
    provider: str,
    current_user=Depends(get_current_active_user),
):
    integrations = _integrations_db.get(current_user.id, [])
    _integrations_db[current_user.id] = [i for i in integrations if i["provider"] != provider]
    return {"success": True, "message": f"Disconnected {provider}."}


@router.get("/{provider}/oauth-url")
def get_oauth_url(
    provider: str,
    current_user=Depends(get_current_active_user),
):
    if provider not in _PROVIDERS:
        return {"success": False, "message": f"Unknown provider: {provider}"}
    state = str(uuid4())
    return {
        "success": True,
        "data": OAuthUrlResponse(
            url=f"https://{provider}.com/oauth/authorize?client_id=placeholder&state={state}",
            provider=provider,
            state=state,
        ).model_dump(),
    }


def _is_connected(user_id: int, provider: str) -> bool:
    integrations = _integrations_db.get(user_id, [])
    return any(i["provider"] == provider and i["is_connected"] for i in integrations)
