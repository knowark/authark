from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ....domain.models import User


class IdentitySupplier(ABC):

    @abstractmethod
    async def identify(self, email: str, password) -> User:
        """Identify method to be implemented."""
