from socket import CAN_BCM_RX_CHECK_DLC
from fastapi import APIRouter, Cookie
from fastapi.responses import RedirectResponse

from core.discord import DiscordOauth2

from os import getenv
from threading import Thread
from time import sleep, time

from typing import Union


router = APIRouter(prefix="/dashboard")
oauth = DiscordOauth2(getenv("CLIENT_ID"), getenv("CLIENT_SECRET"))
cache_users = {}
cache_user_guilds = {}

class CacheManager(Thread):
    def __init__(self):
        super().__init__()
        self.daemon: bool = True

    def run(self):
        while True:
            for token in cache_users:
                if cache_users[token]["expire"] > time():
                    del cache_users[token]
            for token in cache_user_guilds:
                if cache_user_guilds[token]["expire"] > time():
                    del cache_user_guilds[token]
            sleep(300)

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
async def me(token: Union[str, None] = Cookie(default=None)):
    if token is None:
        return {"status": False, "message": "Please login"}
    else:
        if token in cache_users:
            user = cache_users[token]
        else:
            user = await oauth.fetch_user(token)
            user["expire"] = time()
            cache_users[token] = user
        data = {"status": True, "message": None}
        data.update(user)
        return data
    
@router.get("/me/guilds")
async def guilds(token: Union[str, None] = Cookie(default=None)):
    if token is None:
        return {"status": False, "message": "Please login"}
    else:
        if token in cache_user_guilds:
            user = cache_user_guilds[token]
        else:
            user = await oauth.fetch_user(token)
            user["expire"] = time()
            cache_user_guilds[token] = user
        data = {"status": True, "message": None}
        data.update(user)
        return data

@router.get("/login")
def login():
    return RedirectResponse("https://discord.com/api/oauth2/authorize?client_id=1002877676526239794&redirect_uri=https%3A%2F%2Fapi.mc-fdc.com%2Fdashboard%2Fredirect&response_type=code&scope=identify%20guilds")
