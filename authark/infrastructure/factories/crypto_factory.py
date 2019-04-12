from ..config import Config
from ..crypto import (
    PasslibHashService, PyJWTAccessTokenService,
    PyJWTRefreshTokenService)
from .memory_factory import MemoryFactory
from ...application.utilities import ExpressionParser
from ...application.repositories import (
    UserRepository,
    CredentialRepository)
from ...application.services import (
    HashService, TokenService, AccessService)
from ...application.coordinators import (
    AuthCoordinator)


class CryptoFactory(MemoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.path = self.config.get('database', {}).get('url')
        self.access_config = self.config.get('tokens', {}).get('access')
        self.refresh_config = self.config.get('tokens', {}).get('refresh')

    # Services

    def passlib_hash_service(self) -> PasslibHashService:
        return PasslibHashService()

    def pyjwt_access_token_service(self) -> PyJWTAccessTokenService:
        return PyJWTAccessTokenService(
            self.access_config['secret'],
            self.access_config['algorithm'],
            self.access_config['lifetime'])

    def pyjwt_refresh_token_service(self) -> PyJWTRefreshTokenService:
        return PyJWTRefreshTokenService(
            self.refresh_config['secret'],
            self.refresh_config['algorithm'],
            self.refresh_config['lifetime'],
            self.refresh_config['threshold'])
