from fastapi import WebSocket
from typing import List, Dict
import json

class ConnectionManager:
    def __init__(self):
        # Store active connections: chat_id -> List[WebSocket]
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: int):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)
        print(f"WS: Client connected to chat {chat_id}. Total: {len(self.active_connections[chat_id])}")

    def disconnect(self, websocket: WebSocket, chat_id: int):
        if chat_id in self.active_connections:
            if websocket in self.active_connections[chat_id]:
                self.active_connections[chat_id].remove(websocket)
                print(f"WS: Client disconnected from chat {chat_id}. Total: {len(self.active_connections[chat_id])}")
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]

    async def broadcast(self, message: dict, chat_id: int):
        if chat_id in self.active_connections:
            print(f"WS: Broadcasting to {len(self.active_connections[chat_id])} clients in chat {chat_id}")
            for connection in self.active_connections[chat_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"WS: Error sending message: {e}")
                    # Ideally remove dead connection here, but disconnect() handles it on close
