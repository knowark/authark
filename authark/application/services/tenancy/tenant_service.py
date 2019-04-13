from abc import ABC, abstractmethod
from typing import List, Dict, Any
from threading import local
from .catalog_service import CatalogService
from .tenant import Tenant


class TenantService(ABC):
    """Tenant service."""

    @abstractmethod
    def setup(self, tenant: Tenant) -> None:
        "Setup current tenant method to be implemented."


class StandardTenantService(TenantService):

    def __init__(self) -> None:
        self.state = local()
        self.state.__dict__.setdefault('tenant', None)

    def setup(self, tenant: Tenant) -> None:
        self.state.tenant = tenant

    def get_tenant(self) -> Tenant:
        return self.state.tenant
