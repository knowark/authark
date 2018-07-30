import json
from typing import Dict
from abc import ABC, abstractmethod
from authark.application.models.token import Token


class TokenService(ABC):
    @abstractmethod
    def generate_token(self, payload: Dict[str, str]) -> Token:
        "Generate method to be implemented."


class MemoryTokenService(TokenService):
    def generate_token(self, payload: Dict[str, str]) -> Token:
        return Token(json.dumps(payload))
