import os
from ....application.coordinators import SessionCoordinator
from ....application.utilities import ExpressionParser, TenantProvider
from ....application.repositories import UserRepository
from ....application.services import HashService, TokenService
from ...web.middleware import Authenticate
from ..configuration import Config
from ..crypto import JwtSupplier
from .json_factory import JsonFactory
from ..configuration import Config
from ..tenancy import TenantSupplier, MemoryTenantSupplier
from .crypto_factory import CryptoFactory


class WebFactory(CryptoFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def middleware_authenticate(
            self, jwt_supplier: JwtSupplier,
            tenant_supplier: TenantSupplier,
            session_coordinator: SessionCoordinator) -> Authenticate:
        return Authenticate(
            jwt_supplier, tenant_supplier, session_coordinator)