from typing import Dict, List, Optional, Any
from ..services import (TokenService, CatalogService,
                        ProvisionService, Tenant)
from ..repositories import (
    UserRepository, CredentialRepository, RoleRepository,
    RankingRepository, DominionRepository)
from .errors import TenantAlreadyExistsError


class SetupCoordinator:
    def __init__(self, catalog_service: CatalogService,
                 provision_service: ProvisionService,
                 token_service: TokenService) -> None:
        self.catalog_service = catalog_service
        self.provision_service = provision_service
        self.token_service = token_service

    def setup_server(self):
        self.catalog_service.setup()
        self.provision_service.setup()

    def create_tenant(self, tenant_dict: Dict[str, Any]) -> None:
        tenant = Tenant(**tenant_dict)
        domain = ['|', ('slug', '=', tenant.slug),
                  ('name', '=', tenant.name)]
        duplicates = self.catalog_service.search_tenants(  # type: ignore
            domain)

        if duplicates:
            raise TenantAlreadyExistsError(
                f'A tenant with slug "{tenant.slug}" already exists.')

        tenant = self.catalog_service.add_tenant(tenant)
        self.provision_service.provision_tenant(tenant)

    def generate_tenant_token(self, tenant_id: str) -> str:
        tenant = self.catalog_service.get_tenant(tenant_id)
        token = self.token_service.generate_token(vars(tenant))
        return token.value
