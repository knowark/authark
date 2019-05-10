import time
import datetime
from typing import Dict, Union, Any
from ..services import TenantService, Tenant


class SessionCoordinator:
    def __init__(self, tenant_service: TenantService) -> None:
        self.tenant_service = tenant_service

    def set_tenant(self, tenant_dict: Dict[str, Any]) -> None:
        tenant = Tenant(**tenant_dict)
        self.tenant_service.setup(tenant)
