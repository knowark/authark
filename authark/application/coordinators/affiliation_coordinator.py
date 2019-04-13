from typing import Dict, Any
from ..services import TenantService, CatalogService, Tenant
from .types import DominionDict, RoleDict


class AffiliationCoordinator:

    def __init__(self, catalog_service: CatalogService,
                 tenant_service: TenantService) -> None:
        self.catalog_service = catalog_service
        self.tenant_service = tenant_service

    def establish_tenant(self, tenant_dict: Dict[str, Any]) -> None:
        slug = tenant_dict.get('slug', '')
        domain = [('slug', '=', slug)]
        tenants = self.catalog_service.search_tenants(domain)

        if not len(tenants) == 1:
            raise ValueError("Your tenant was not found.")

        tenant = tenants[0]
        self.tenant_service.setup(tenant)
