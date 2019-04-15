import json
from typing import Dict, Any
from abc import ABC, abstractmethod
from authark.application.models import Token


class TokenService(ABC):
    @abstractmethod
    def generate_token(self, payload: Dict[str, str]) -> Token:
        "Generate method to be implemented."

    @abstractmethod
    def valid(self, token: Token) -> bool:
        "Valid method to be implemented."

    @abstractmethod
    def renew(self, token: Token) -> bool:
        "Renew method to be implemented."


class MemoryTokenService(TokenService):
    def generate_token(self, payload: Dict[str, Any]) -> Token:
        return Token(json.dumps(payload))

    def valid(self, token: Token) -> bool:
        return True

    def renew(self, token: Token) -> bool:
        return False

# Dedicated Aliases


class AccessTokenService(TokenService):
    """Access Token Service"""


class MemoryAccessTokenService(MemoryTokenService, AccessTokenService):
    """Access Token Service"""


class RefreshTokenService(TokenService):
    """Refresh Token Service"""


class MemoryRefreshTokenService(MemoryTokenService, RefreshTokenService):
    """Memory Refresh Token Service"""
