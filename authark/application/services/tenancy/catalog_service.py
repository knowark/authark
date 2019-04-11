from uuid import uuid4
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from .tenant import Tenant


class CatalogService(ABC):
    """Tenant Catalog service."""

    @abstractmethod
    def setup(self) -> bool:
        "Setup method to be implemented."

    @abstractmethod
    def add_tenant(self, tenant: Tenant) -> Tenant:
        "Add tenant method to be implemented."


class MemoryCatalogService(CatalogService):

    def __init__(self) -> None:
        self.catalog: Optional[Dict] = None

    def setup(self) -> bool:
        self.catalog = {}
        return True

    def add_tenant(self, tenant: Tenant) -> Tenant:
        tenant.id = tenant.id or str(uuid4())
        self.catalog[tenant.id] = tenant
        return tenant
