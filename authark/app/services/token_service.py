from typing import Dict
from abc import ABC, abstractmethod
from authark.app.models.token import Token


class TokenService(ABC):
    @abstractmethod
    def generate_token(self, payload: Dict[str, str] = None) -> Token:
        ...
