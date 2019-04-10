from typing import List, Optional, Any
from ..services import CatalogService, ProvisionService
from ..repositories import (
    UserRepository, CredentialRepository, RoleRepository,
    RankingRepository, DominionRepository)
from ..models import User, Credential, Role, Ranking, Dominion


class SetupCoordinator:
    def __init__(self, catalog_service: CatalogService,
                 provision_service: ProvisionService) -> None:
        self.catalog_service = catalog_service
        self.provision_service = provision_service

    def setup_catalog(self):
        self.catalog_service.setup()

    def create_tenant(self, args):
        self.catalog_service = catalog_service
        self.provision_service = provision_service
        pass
