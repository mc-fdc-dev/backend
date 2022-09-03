from fastapi import APIRouter, Cookie, Request, HTTPException
from fastapi.responses import RedirectResponse

from core.discord import DiscordOauth2

from os import getenv
from threading import Thread
from time import sleep, time

from typing import Union


router = APIRouter(prefix="/dashboard")
oauth = DiscordOauth2(getenv("CLIENT_ID"), getenv("CLIENT_SECRET"))
cache_users = {}
cooldowns = {}

class CacheManager(Thread):
    def __init__(self):
        super().__init__()
        self.daemon: bool = True

    def run(self):
        while True:
            for token in cache_users:
                if cache_users[token]["expire"] > time():
                    del cache_users[token]
            sleep(600)

cache = CacheManager()
cache.start()

@router.get("/")
def main():
    return {"message": "Hello, World", "status": True}

@router.get("/redirect")
async def redirect(code: str):
    token = await oauth.exchange_code(code)
    response = RedirectResponse("https://mc-fdc.com/dashboard")
    response.set_cookie("token", token.access, expires=token.expires_in)
    return response

@router.get("/me")
async def me(request: Request, token: Union[str, None] = Cookie(default=None)):
    if request.client.host in cooldowns:
        if cooldowns[request.client.host] > time():
            raise HTTPException(status_code=403, detail="Too many access")
    cooldowns[request.client.host] = time() + 30
    if token is None:
        return {"status": False, "message": "Please login"}
    else:
        if token in cache_users:
            user = cache_users[token]
        else:
            user = {
                "user": await oauth.fetch_user(token),
                "guilds": await oauth.fetch_guilds(token),
                "expire": time()
            }
            cache_users[token] = user
        data = {"status": True, "message": None}
        data.update(user)
        del data["expire"]
        return data

@router.get("/me/guilds/{guildid}")
async def get_guild(req: Request, guildid: int):
    async with req.app.state.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Guild WHERE GuildId=%s;", (guildid,))
            guildid, name, icon = await cur.fetchone()
    return {"status": True}

@router.get("/login")
def login():
    return RedirectResponse("https://discord.com/api/oauth2/authorize?client_id=1002877676526239794&redirect_uri=https%3A%2F%2Fapi.mc-fdc.com%2Fdashboard%2Fredirect&response_type=code&scope=identify%20guilds")
