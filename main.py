from fastapi import FastAPI, WebSocket
from aiomysql import create_pool

from core import managers

from typing import List
from os import listdir

app = FastAPI()
app.state.backend: managers.WsManager = managers.WsManager()

for router in listdir("routers"):
    app.include_router(router.router)

@app.on_event("startup")
async def _startup():
    app.state.pool = await create_pool(host=secret.DB_URL, port=3306, user=secret.DB_USERNAME, password=secret.DB_PASSWORD, db=secret.DB_DATABASE)
    print("startup done")

@app.get("/")
def main():
    return {"status": 200, "message": "Hello, World"}
