from ...config import Config
from ...crypto import (
    PasslibHashService, PyJWTTokenService)
from .memory_factory import MemoryFactory


class CryptoFactory(MemoryFactory):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.path = config['database']['url']

    # Services

    def passlib_hash_service(self) -> PasslibHashService:
        return PasslibHashService()

    def pyjwt_token_service(self) -> PyJWTTokenService:
        return PyJWTTokenService()
