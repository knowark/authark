from typing import List, Optional, Any
from ..services import CatalogService, ProvisionService, Tenant
from ..repositories import (
    UserRepository, CredentialRepository, RoleRepository,
    RankingRepository, DominionRepository)
from .errors import TenantAlreadyExistsError


class SetupCoordinator:
    def __init__(self, catalog_service: CatalogService,
                 provision_service: ProvisionService) -> None:
        self.catalog_service = catalog_service
        self.provision_service = provision_service

    def setup_server(self):
        self.catalog_service.setup()
        self.provision_service.setup()

    def create_tenant(self, tenant_dict):
        tenant = Tenant(**tenant_dict)
        domain = ['|', ('slug', '=', tenant.slug),
                  ('name', '=', tenant.name)]
        duplicates = self.catalog_service.search_tenants(domain)
        if duplicates:
            raise TenantAlreadyExistsError()
        self.catalog_service.add_tenant(tenant)
        self.provision_service.create_tenant(tenant)
