from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ....domain.models import User
from .identity_supplier import IdentitySupplier


class MemoryIdentitySupplier(IdentitySupplier):

    async def identify(self, email: str, password) -> User:
        return User(email=email)
