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
            await self.send_heartbeat()
            await self.wait_heartbeat()
            await asyncio.sleep(60)
    
    async def send_heartbeat(self):
        await self.manager.send("heartbeat", "ping")
    
    async def wait_heartbeat(self):
        try:
            data = await asyncio.wait_for(self.manager.recv(), timeout=10)
            print(data)
            if data["type"] == "heartbeat":
                if data["data"] == "pong":
                    await self.manager.send("heartbeat", "success")
                else:
                    await self.manager.send("heartbeat", "invalid")
                    await self.wait_heartbeat()
            else:
                await self.wait_heartbeat()
        except asyncio.TimeoutError:
            await self.manager.close(message="Please send heartbeat")
            self.closed = True

class WsManager:
    def __init__(self):
        self.active_connection: WebSocket | None = None

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.heartbeat = HeartBeat(self)
        self.active_connection = websocket

    async def disconnect(self):
        self.heartbeat.close()
        try:
            await self.active_connection.close()
        except Exception:
            pass
        self.active_connection = None

    async def send(self, type: str, data: Any, **kwargs):
        await self.active_connection.send_json({"type": type, "data": data}, **kwargs)

    async def recv(self) -> dict:
        return await self.active_connection.receive_json(mode="text")
    
    @property
    def closed(self):
        return self.heartbeat.closed
