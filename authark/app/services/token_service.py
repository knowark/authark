import json
from typing import Dict
from abc import ABC, abstractmethod
from authark.app.models.token import Token


class TokenService(ABC):
    @abstractmethod
    def generate_token(self, payload: Dict[str, str] = None) -> Token:
        "Generate method to be implemented."


class MemoryTokenService(TokenService):
    def generate_token(self, payload: Dict[str, str] = None) -> Token:
        return Token(json.dumps(payload))
