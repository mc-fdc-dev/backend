from fastapi import APIRouter, WebSocket, Request
from orjson import loads, dumps

from typing import TypedDict, Any
from core import managers
from os import getenv


router = APIRouter()

class BackendData(TypedDict):
    type: str
    data: Any

@router.websocket("/backend")
async def backend(req: Request, ws: WebSocket):
    backend = request.state.backend
    await backend.connect(ws)
    while True:
        data: BackendData = loads(await ws.receive_text())
        if data["type"] == "hello":
            if data["data"] == getenv("BACKEND_PASSWORD"):
                await backend.send(type="success", data=None)
            else:
                await backend.disconnect()
