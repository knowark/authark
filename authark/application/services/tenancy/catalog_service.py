from uuid import uuid4
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ...utilities import ExpressionParser
from .tenant import Tenant
from .types import QueryDomain


class CatalogService(ABC):
    """Tenant Catalog service."""

    @abstractmethod
    def setup(self) -> bool:
        "Setup method to be implemented."

    @abstractmethod
    def add_tenant(self, tenant: Tenant) -> Tenant:
        "Add tenant method to be implemented."

    @abstractmethod
    def search_tenants(self, domain: QueryDomain) -> List[Tenant]:
        "Search tenants method to be implemented."


class MemoryCatalogService(CatalogService):

    def __init__(self, parser: ExpressionParser) -> None:
        self.catalog: Optional[Dict] = None
        self.parser = parser

    def setup(self) -> bool:
        self.catalog = {}
        return True

    def add_tenant(self, tenant: Tenant) -> Tenant:
        tenant.id = tenant.id or str(uuid4())
        if self.catalog is None:
            raise ValueError("Setup the tenant catalog first.")
        self.catalog[tenant.id] = tenant
        return tenant

    def search_tenants(self, domain: QueryDomain) -> List[Tenant]:
        tenants = []
        filter_function = self.parser.parse(domain)
        if self.catalog is None:
            raise ValueError("Setup the tenant catalog first.")
        for tenant in list(self.catalog.values()):
            if filter_function(tenant):
                tenants.append(tenant)

        return tenants
