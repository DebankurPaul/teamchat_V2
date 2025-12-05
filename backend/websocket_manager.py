from fastapi import WebSocket
from typing import Dict, List
import json

class ConnectionManager:
    def __init__(self):
        # user_id -> WebSocket
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        await self.broadcast_status(user_id, "online")

    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        # We can't await here easily if it's not async, but usually disconnect is called from async endpoint
        # For now, we'll handle the broadcast in the endpoint

    async def broadcast(self, message: str, sender_id: str = None):
        for user_id, connection in self.active_connections.items():
            if user_id != sender_id:
                try:
                    await connection.send_text(message)
                except:
                    pass

    async def broadcast_status(self, user_id: str, status: str):
        status_msg = json.dumps({
            "type": "status_update",
            "userId": user_id,
            "status": status
        })
        for connection in self.active_connections.values():
            try:
                await connection.send_text(status_msg)
            except:
                pass
