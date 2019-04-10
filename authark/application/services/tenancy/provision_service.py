from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .tenant import Tenant


class ProvisionService(ABC):
    """Tenant Provision service."""


class MemoryProvisionService(ProvisionService):

    def __init__(self) -> None:
        pass
