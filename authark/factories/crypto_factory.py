from ..application.domain.services import (
    HashService, AccessTokenService, RefreshTokenService,
    VerificationTokenService, TokenService)
from ..core.suppliers.crypto import (
    PasslibHashService, PyJWTTokenService,
    PyJWTVerificationTokenService, PyJWTAccessTokenService,
    PyJWTRefreshTokenService)
from ..core.common import Config
from .base_factory import BaseFactory


class CryptoFactory(BaseFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.path = self.config.get('database', {}).get('url')
        self.tenant_config = self.config.get('tokens', {}).get('tenant')
        self.access_config = self.config.get('tokens', {}).get('access')
        self.refresh_config = self.config.get('tokens', {}).get('refresh')
        self.verification_config = self.config.get(
            'tokens', {}).get('verification')

    # Services

    def hash_service(self) -> HashService:
        return PasslibHashService()

    def token_service(self) -> TokenService:
        return PyJWTTokenService(
            self.tenant_config['secret'],
            self.tenant_config['algorithm'],
            self.tenant_config['lifetime'])

    def access_token_service(self) -> AccessTokenService:
        return PyJWTAccessTokenService(
            self.access_config['secret'],
            self.access_config['algorithm'],
            self.access_config['lifetime'])

    def verification_token_service(self) -> VerificationTokenService:
        return PyJWTVerificationTokenService(
            self.verification_config['secret'],
            self.verification_config['algorithm'],
            self.verification_config['lifetime'])

    def refresh_token_service(self) -> RefreshTokenService:
        return PyJWTRefreshTokenService(
            self.refresh_config['secret'],
            self.refresh_config['algorithm'],
            self.refresh_config['lifetime'],
            self.refresh_config['threshold'])
