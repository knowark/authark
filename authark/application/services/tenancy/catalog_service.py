from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from .tenant import Tenant


class CatalogService(ABC):
    """Tenant Catalog service."""

    @abstractmethod
    def setup(self) -> bool:
        "Setup method to be implemented."


class MemoryCatalogService(CatalogService):

    def __init__(self) -> None:
        self.catalog: Optional[Dict] = None

    def setup(self) -> bool:
        self.catalog = {}
        return True
