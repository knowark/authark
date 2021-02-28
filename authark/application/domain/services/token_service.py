import json
from typing import Dict, Any
from abc import ABC, abstractmethod
from ..models import Token


class TokenService(ABC):
    @abstractmethod
    def generate_token(self, payload: Dict[str, str]) -> Token:
        "Generate method to be implemented."

    @abstractmethod
    def valid(self, token: Token) -> bool:
        "Valid method to be implemented."

    @abstractmethod
    def decode(self, token: Token) -> Dict[str, Any]:
        "Decode method to be implemented."


class MemoryTokenService(TokenService):
    def generate_token(self, payload: Dict[str, Any]) -> Token:
        return Token(json.dumps(payload))

    def valid(self, token: Token) -> bool:
        return True

    def decode(self, token: Token) -> Dict[str, Any]:
        return json.loads(token.value)


# Dedicated Aliases


class AccessTokenService(TokenService):
    """Access Token Service"""


class MemoryAccessTokenService(MemoryTokenService, AccessTokenService):
    """Access Token Service"""


class RefreshTokenService(TokenService):
    """Refresh Token Service"""


class MemoryRefreshTokenService(MemoryTokenService, RefreshTokenService):
    """Memory Refresh Token Service"""


class VerificationTokenService(TokenService):
    """Verification Token Service"""


class MemoryVerificationTokenService(
        MemoryTokenService, VerificationTokenService):
    """Memory Verification Token Service"""
