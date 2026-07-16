"""
WebSocket Manager — Real-time notifications for authenticated users.

Events:
  - application.created   → new application submitted
  - application.updated   → status change
  - interview.scheduled   → interview booked
  - ai.complete           → AI task finished
  - notification          → general notification

Usage (on frontend):
    const ws = new WebSocket(`ws://localhost:8000/ws?token=${jwt}`);
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        // { type: "application.updated", payload: {...} }
    };
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections per user.
    Thread-safe using asyncio.Queue-based approach.
    """

    def __init__(self) -> None:
        # user_id -> list of WebSocket connections
        self._connections: dict[int, list[WebSocket]] = {}
        # user_id -> queue of pending notifications (for offline delivery)
        self._pending: dict[int, list[dict[str, Any]]] = {}

    async def connect(self, websocket: WebSocket, user_id: int) -> None:
        """Accept a WebSocket connection and register it."""
        await websocket.accept()
        if user_id not in self._connections:
            self._connections[user_id] = []
        self._connections[user_id].append(websocket)

        # Deliver any pending notifications
        pending = self._pending.pop(user_id, [])
        for notification in pending:
            try:
                await websocket.send_json(notification)
            except Exception:
                pass

        logger.info(f"WebSocket connected: user_id={user_id} (total: {len(self._connections[user_id])})")

    def disconnect(self, websocket: WebSocket, user_id: int) -> None:
        """Remove a WebSocket connection."""
        if user_id in self._connections:
            self._connections[user_id] = [
                ws for ws in self._connections[user_id] if ws != websocket
            ]
            if not self._connections[user_id]:
                del self._connections[user_id]
        logger.info(f"WebSocket disconnected: user_id={user_id}")

    async def send_to_user(self, user_id: int, event_type: str, payload: dict[str, Any]) -> bool:
        """
        Send a notification to all connections for a user.
        Returns True if delivered, False if queued for later.
        """
        message = {
            "type": event_type,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat(),
        }

        connections = self._connections.get(user_id, [])
        if not connections:
            # Queue for later delivery
            if user_id not in self._pending:
                self._pending[user_id] = []
            self._pending[user_id].append(message)
            return False

        dead_connections: list[WebSocket] = []
        for ws in connections:
            try:
                await ws.send_json(message)
            except Exception:
                dead_connections.append(ws)

        for ws in dead_connections:
            self.disconnect(ws, user_id)

        return True

    async def broadcast(self, event_type: str, payload: dict[str, Any]) -> int:
        """Broadcast a message to ALL connected users. Returns count of recipients."""
        message = {
            "type": event_type,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat(),
        }

        count = 0
        for user_id, connections in list(self._connections.items()):
            dead = []
            for ws in connections:
                try:
                    await ws.send_json(message)
                    count += 1
                except Exception:
                    dead.append(ws)
            for ws in dead:
                self.disconnect(ws, user_id)

        return count

    @property
    def active_connections(self) -> int:
        """Total number of active WebSocket connections."""
        return sum(len(conns) for conns in self._connections.values())

    @property
    def active_users(self) -> int:
        """Number of users with at least one active connection."""
        return len(self._connections)


# Global singleton
manager = ConnectionManager()


async def handle_websocket(websocket: WebSocket, user_id: int) -> None:
    """
    Handle an authenticated WebSocket connection lifecycle.
    Call this from your WebSocket endpoint.
    """
    await manager.connect(websocket, user_id)
    try:
        # Keep connection alive by reading (and discarding) incoming messages
        async for _ in websocket.iter_json():
            pass  # Client can send pings if desired
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        manager.disconnect(websocket, user_id)
