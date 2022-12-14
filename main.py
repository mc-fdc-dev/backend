from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from aiomysql import create_pool

from core import managers

from os import listdir, getenv
from importlib import import_module

app = FastAPI()
app.state.backend: managers.WsManager = managers.WsManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mc-fdc.com",
        "http://mc-fdc.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router_path in listdir("./routers"):
    if router_path.startswith("__"):
        continue
    app.include_router(import_module(f"routers.{router_path[:-3]}").router)

@app.on_event("startup")
async def _startup():
    app.state.pool = await create_pool(
        host=getenv("DB_HOST"), port=3306, user=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"), db=getenv("DB_NAME")
    )
    print("startup done")

@app.get("/")
def main():
    return {"status": 200, "message": "Hello, World"}

if __name__ == "__main__":
    print("Running at {}".format(getenv("PORT")))
    uvicorn.run("main:app", host="0.0.0.0", port=int(getenv("PORT", "8080")))
