from fastapi import WebSocket


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
