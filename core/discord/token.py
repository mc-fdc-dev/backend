from typing import Dict

class Token:
    def __init__(self, data: Dict[str, str], oauth: "DiscordOauth"):
        self.__data = data

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
    def expires_in(self) -> int:
        return int(self.__data["expires_in"])
