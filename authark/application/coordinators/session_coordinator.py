from typing import Dict, Any
from ..services import TenantService, Tenant


class SessionCoordinator:
    def __init__(self, tenant_service: TenantService) -> None:
        self.tenant_service = tenant_service

    def set_tenant(self, tenant_dict: Dict[str, Any]) -> None:
        tenant = Tenant(**tenant_dict)
        self.tenant_service.setup(tenant)

    def get_tenant(self) -> Dict[str, Any]:
        tenant = self.tenant_service.tenant
        return vars(tenant)
