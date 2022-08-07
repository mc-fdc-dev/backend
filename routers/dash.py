from fastapi import APIRouter, Cookie
from fastapi.responses import RedirectResponse

from core.discord import DiscordOauth2

from os import getenv

from typing import Union


router = APIRouter(prefix="/dashboard")
oauth = DiscordOauth2(getenv("CLIENT_ID"), getenv("CLIENT_SECRET"))


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
        data = {"status": True, "message": None}
        data.update(await oauth.fetch_user(token))
        return data
