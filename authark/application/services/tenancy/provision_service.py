from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .tenant import Tenant


class ProvisionService(ABC):
    """Tenant Provision service."""

    @abstractmethod
    def setup(self) -> bool:
        "Setup method to be implemented."


class MemoryProvisionService(ProvisionService):

    def __init__(self) -> None:
        self.pool: Dict = None

    def setup(self) -> bool:
        self.pool = {}
        return True
