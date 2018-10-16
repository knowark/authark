import json
from typing import Dict, Any
from abc import ABC, abstractmethod
from authark.application.models.token import Token


class TokenService(ABC):
    @abstractmethod
    def generate_token(self, payload: Dict[str, str]) -> Token:
        "Generate method to be implemented."

    @abstractmethod
    def valid(self, Token) -> bool:
        "Valid method to be implemented."

    @abstractmethod
    def renew(self, Token) -> bool:
        "Renew method to be implemented."


class MemoryTokenService(TokenService):
    def generate_token(self, payload: Dict[str, Any]) -> Token:
        return Token(json.dumps(payload))

    def valid(self, Token) -> bool:
        return True

    def renew(self, Token) -> bool:
        return False
