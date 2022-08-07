from fastapi import APIRouter, WebSocket, Request
from orjson import loads, dumps

from typing import TypedDict, Any
from core import managers
from os import getenv
from asyncio import wait_for, TimeoutError


router = APIRouter()

class BackendData(TypedDict):
    type: str
    data: Any

@router.websocket("/backend")
async def backend(ws: WebSocket):
    backend = ws.app.state.backend
    await backend.connect(ws)
    try:
        data: BackendData = loads(await wait_for(ws.receive_text(), timeout=60))
    except TimeoutError:
        if data["type"] == "login":
            if data["data"] == getenv("BACKEND_PASSWORD"):
                await backend.send(type="success", data=None)
                print("Logined")
            else:
                await backend.disconnect(message="Password is invalid")
        else:
            await backend.disconnect(message="Please login first")
    while True:
        data: BackendData = loads(await ws.receive_text())
        print(data)
