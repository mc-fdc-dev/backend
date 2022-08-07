from fastapi import WebSocket

from typing import Any


class WsManagerError(Exception):
    pass

class WsManager:
    def __init__(self):
        self.active_connection: WebSocket | None = None

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connection = websocket

    async def disconnect(self):
        try:
            await self.active_connection.close()
        except Exception:
            pass
        self.active_connection = None

    async def send(self, type: str, data: Any):
        await self.active_connection.send_text(dumps({"type": type, "data": data}))
