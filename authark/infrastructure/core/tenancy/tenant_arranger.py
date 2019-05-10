from typing import List, Optional, Any
from ..services import ExportService, CatalogService
from ..repositories import (
    UserRepository, CredentialRepository, RoleRepository, RankingRepository,
    DominionRepository)
from ..models import User, Credential, Role, Ranking, Dominion


class ExportCoordinator:
    def __init__(self, export_service: ExportService,
                 catalog_service: CatalogService) -> None:
        self.export_service = export_service
        self.catalog_service = catalog_service

    def export_tenants(self, tenant_ids: List[str]) -> None:
        tenants = []
        for tenant_id in tenant_ids:
            tenant = self.catalog_service.get_tenant(tenant_id)
            tenants.append(tenant)
        self.export_service.export_tenants(tenants)
