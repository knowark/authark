from abc import ABC, abstractmethod
from authark.app.models.token import Token


class TokenService(ABC):
    @abstractmethod
    def generate_token(self) -> Token:
        ...
