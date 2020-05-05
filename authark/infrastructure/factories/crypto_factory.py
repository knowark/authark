from ..core.suppliers.crypto import (
    PasslibHashService, PyJWTTokenService, JwtSupplier,
    PyJWTAccessTokenService, PyJWTRefreshTokenService)
from ..core.common import Config
from .base_factory import BaseFactory


class CryptoFactory(BaseFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.path = self.config.get('database', {}).get('url')
        self.tenant_config = self.config.get('tokens', {}).get('tenant')
        self.access_config = self.config.get('tokens', {}).get('access')
        self.refresh_config = self.config.get('tokens', {}).get('refresh')

    # Services

    def passlib_hash_service(self) -> PasslibHashService:
        return PasslibHashService()

    def pyjwt_token_service(self) -> PyJWTTokenService:
        return PyJWTTokenService(
            self.tenant_config['secret'],
            self.tenant_config['algorithm'],
            self.tenant_config['lifetime'])

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

    def jwt_supplier(self) -> JwtSupplier:
        secret = self.access_config['secret']
        return JwtSupplier(secret)
