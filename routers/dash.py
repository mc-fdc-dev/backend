from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from core.discord import DiscordOauth2

from os import getenv


router = APIRouter(prefix="/dashboard")
oauth = DiscordOauth2(getenv("CLIENT_ID"), getenv("CLIENT_SECRET"))


@router.get("/")
def main():
    return {"message": "Hello, World", "status": 200}

@router.get("/redirect")
async def redirect(code: str):
    token = await oauth.exchange_code(code)
    response = RedirectResponse("https://mc-fdc.com/dashboard")
    response.set_cookie("token", token.access, expires=token.expires_in)
    return response
