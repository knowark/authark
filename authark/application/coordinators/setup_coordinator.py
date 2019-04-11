from typing import List, Optional, Any
from ..services import CatalogService, ProvisionService, Tenant
from ..repositories import (
    UserRepository, CredentialRepository, RoleRepository,
    RankingRepository, DominionRepository)


class SetupCoordinator:
    def __init__(self, catalog_service: CatalogService,
                 provision_service: ProvisionService) -> None:
        self.catalog_service = catalog_service
        self.provision_service = provision_service

    def setup_catalog(self):
        self.catalog_service.setup()
        self.provision_service.setup()

    def create_tenant(self, tenant_dict):
        self.catalog_service = catalog_service
        if self.catalog_service.get(''):
            return False
        self.provision_service = provision_service
        pass
