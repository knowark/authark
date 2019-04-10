from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .tenant import Tenant


class CatalogService(ABC):
    """Tenant Catalog service."""


class MemoryCatalogService(CatalogService):

    def __init__(self) -> None:
        pass
