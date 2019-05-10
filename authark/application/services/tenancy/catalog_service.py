from uuid import uuid4
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ...utilities import ExpressionParser
from .tenant import Tenant
from .types import QueryDomain


class CatalogService(ABC):
    """Tenant Catalog service."""

    @abstractmethod
    def add_tenant(self, tenant: Tenant) -> Tenant:
        "Add tenant method to be implemented."

    @abstractmethod
    def get_tenant(self, tenant_id: str) -> Tenant:
        "Get tenant method to be implemented."

    @abstractmethod
    def search_tenants(self, domain: QueryDomain) -> List[Tenant]:
        "Search tenants method to be implemented."


class MemoryCatalogService(CatalogService):

    def __init__(self, parser: ExpressionParser) -> None:
        self.parser = parser
        self.catalog: Dict[str, Tenant] = {}

    def add_tenant(self, tenant: Tenant) -> Tenant:
        self.catalog[tenant.id] = tenant
        return tenant

    def get_tenant(self, tenant_id: str) -> Tenant:
        tenant = self.catalog.get(tenant_id)

        if not tenant:
            raise ValueError('Tenant not found.')

        return tenant

    def search_tenants(self, domain: QueryDomain) -> List[Tenant]:
        tenants = []
        filter_function = self.parser.parse(domain)
        for tenant in list(self.catalog.values()):
            if filter_function(tenant):
                tenants.append(tenant)

        return tenants
