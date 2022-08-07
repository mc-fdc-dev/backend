from fastapi import APIRouter, WebSocket, Request
from orjson import loads, dumps

from typing import TypedDict, Any

router = ApiRouter()

class WsManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send(self, type: str, data: Any, websocket: WebSocket):
        await websocket.send_text(dumps({"type": type, "data": data}))

class BackendData(TypedDict):
    type: str
    data: Any

@router.websocket("/backend")
async def backend(req: Request, ws: WebSocket):
    await ws.accept()
    while True:
        data: BackendData = loads(await ws.receive_text())
        if data["type"] == "hello":
            
