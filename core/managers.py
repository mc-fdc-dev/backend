from fastapi import WebSocket
from orjson import dumps, loads

import asyncio

from typing import Any


class WsManagerError(Exception):
    pass

class HeartBeat:
    closed: bool = False

    def __init__(self, manager):
        self.manager = manager

    def run(self):
        self.task = asyncio.create_task(self.main())
    
    def close(self):
        self.task.cancel()

    async def main(self):
        while True:
            print("Send heartbeat")
            await manager.send("heartbeat", "ping")
            try:
                await asyncio.wait_for(manager.recv(), timeout=10)
            except asyncio.TimeoutError:
                await manager.close(message="Please send heartbeat")
                self.closed = True
            await asyncio.sleep(60)

class WsManager:
    def __init__(self):
        self.active_connection: WebSocket | None = None

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.heartbeat = HeartBeat(self)
        self.heartbeat.run()
        self.active_connection = websocket

    async def disconnect(self):
        self.heartbeat.close()
        try:
            await self.active_connection.close()
        except Exception:
            pass
        self.active_connection = None

    async def send(self, type: str, data: Any, **kwargs):
        await self.active_connection.send_text(dumps({"type": type, "data": data}), **kwargs)

    async def recv(self) -> dict:
        return loads(await self.active_connection.receive_text())
    
    @property
    def closed(self):
        return self.heartbeat.closed
