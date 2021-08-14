from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..models import User


class IdentityService(ABC):

    @abstractmethod
    async def identify(self, provider: str, code: str) -> User:
        """Identify method to be implemented."""


class MemoryIdentityService(IdentityService):
    def __init__(self, user: User = None) -> None:
        self.user = user or User(email="default@memory")

    async def identify(self, provider: str, code: str) -> User:
        return self.user
