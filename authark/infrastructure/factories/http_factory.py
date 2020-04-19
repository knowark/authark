import os
from ...application.coordinators import SessionCoordinator
from ..web.middleware import Authenticate
from ..config import Config
from ..core.tenancy import TenantSupplier
from ..core.crypto import JwtSupplier
from .json_factory import JsonFactory


class HttpFactory(JsonFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def middleware_authenticate(
            self, tenant_supplier: TenantSupplier,
            session_coordinator: SessionCoordinator) -> Authenticate:
        return Authenticate(tenant_supplier, session_coordinator)
