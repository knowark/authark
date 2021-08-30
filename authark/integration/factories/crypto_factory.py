from ...application.domain.services import (
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
        self.tokens_tenant_config = self.config.get(
            'tokens', {}).get('tenant')
        self.tokens_access_config = self.config.get(
            'tokens', {}).get('access')
        self.tokens_refresh_config = self.config.get(
            'tokens', {}).get('refresh')
        self.tokens_verification_config = self.config.get(
            'tokens', {}).get('verification')

    # Services

    def hash_service(self) -> HashService:
        return PasslibHashService()

    def token_service(self) -> TokenService:
        return PyJWTTokenService(
            self.tokens_tenant_config['secret'],
            self.tokens_tenant_config['algorithm'],
            self.tokens_tenant_config['lifetime'])

    def access_token_service(self) -> AccessTokenService:
        return PyJWTAccessTokenService(
            self.tokens_access_config['secret'],
            self.tokens_access_config['algorithm'],
            self.tokens_access_config['lifetime'])

    def verification_token_service(self) -> VerificationTokenService:
        return PyJWTVerificationTokenService(
            self.tokens_verification_config['secret'],
            self.tokens_verification_config['algorithm'],
            self.tokens_verification_config['lifetime'])

    def refresh_token_service(self) -> RefreshTokenService:
        return PyJWTRefreshTokenService(
            self.tokens_refresh_config['secret'],
            self.tokens_refresh_config['algorithm'],
            self.tokens_refresh_config['lifetime'],
            self.tokens_refresh_config['threshold'])
