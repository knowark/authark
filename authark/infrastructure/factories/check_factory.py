import os
from ...application.coordinators import SessionCoordinator
from ...application.utilities import QueryParser, TenantProvider
from ...application.repositories import UserRepository
from ...application.services import HashService, TokenService
from ..web.middleware import Authenticate
from ..config import Config
from ..core.crypto import JwtSupplier
from .json_factory import JsonFactory
from ..config import Config
from ..core.tenancy import TenantSupplier, MemoryTenantSupplier
from .crypto_factory import CryptoFactory


class CheckFactory(CryptoFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def middleware_authenticate(
            self, tenant_supplier: TenantSupplier,
            session_coordinator: SessionCoordinator) -> Authenticate:
        return Authenticate(tenant_supplier, session_coordinator)
