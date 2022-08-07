from httpx import AsyncClient, Response

from .token import Token


class DiscordOauth2:
    BASEURL: str = "https://discord.com/api/v10"
    REDIRECT_URI: str = "https://api.mc-fdc.com/dashboard/redirect"
    def __init__(self, client_id: int, client_secret: str):
        self.client = AsyncClient(base_url=self.BASEURL)
        self.client_id = client_id
        self.client_secret = client_secret

    async def request(self, method: str, path: str, **kwargs) -> Response:
        res = await self.client.request(method, path, **kwargs)
        res.raise_for_status()
        return res

    async def exchange_code(self, code: str) -> Token:
        r = await self.request("POST", "/oauth2/token", data={
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.REDIRECT_URI
        }, headers={
            "Content-Type": "application/x-www-form-urlencoded"
        })
        return Token(r.json(), self)
