from typing import TYPE_CHECKING, Dict

from datetime import datetime, timedelta

if TYPE_CHECKING:
    from .oauth2 import DiscordOauth2

class Token:
    def __init__(self, data: Dict[str, str], oauth: DiscordOauth2):
        self.__data = data
        self._expires_in = datetime.now(
        ) + timedelta(seconds=self.data["expires_in"])

    @property
    def access(self) -> str:
        return self.__data["access_token"]
    
    @property
    def type(self) -> str:
        return self.__data["token_type"]
    
    @property
    def refresh(self) -> str:
        return self.__data["refresh_token"]
    
    @property
    def expires_in(self) -> datetime:
        return self._expires_in
