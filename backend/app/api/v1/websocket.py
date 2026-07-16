"""
WebSocket endpoint for real-time notifications.
Connect: ws://localhost:8000/api/v1/ws?token=YOUR_JWT
"""

from fastapi import APIRouter, Depends, Query, WebSocket
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.security.jwt import decode_token
from backend.app.services.websocket_manager import handle_websocket

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    """WebSocket endpoint for authenticated real-time notifications."""
    # Authenticate via JWT token
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub", 0))
    except Exception:
        await websocket.close(code=4001, reason="Invalid authentication")
        return

    await handle_websocket(websocket, user_id)
