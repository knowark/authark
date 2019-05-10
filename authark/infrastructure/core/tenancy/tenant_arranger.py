# from typing import List, Optional, Any
# from ..services import ExportService, CatalogService
# from ..repositories import (
#     UserRepository, CredentialRepository, RoleRepository, RankingRepository,
#     DominionRepository)
# from ..models import User, Credential, Role, Ranking, Dominion


# class ExportCoordinator:
#     def __init__(self, export_service: ExportService,
#                  catalog_service: CatalogService) -> None:
#         self.export_service = export_service
#         self.catalog_service = catalog_service

#     def export_tenants(self, tenant_ids: List[str]) -> None:
#         tenants = []
#         for tenant_id in tenant_ids:
#             tenant = self.catalog_service.get_tenant(tenant_id)
#             tenants.append(tenant)
#         self.export_service.export_tenants(tenants)


# import json
# from datetime import datetime
# from pathlib import Path
# from typing import List, Any
# from ...application.services import TokenService, ExportService, Tenant


# class JsonExportService(ExportService):

#     def __init__(self, path: str, token_service: TokenService) -> None:
#         self.path = path
#         self.token_service = token_service

#     def export_tenants(self, tenants: List[Tenant]) -> None:
#         export_dict = {}
#         for tenant in tenants:
#             export_dict[tenant.slug] = (
#                 self.token_service.generate_token(vars(tenant)).value)

#         path = Path(self.path)
#         path.mkdir(parents=True, exist_ok=True)

#         now = datetime.now().replace(microsecond=0).isoformat()
#         now = now.replace('-', '').replace('T', '').replace(':', '')
#         filepath = path / f"tenant_tokens_{now}.json"
#         with filepath.open('w') as f:
#             json.dump(export_dict, f, indent=2)
