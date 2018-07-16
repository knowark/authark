from collections import UserDict
from typing import Any, Dict
from authark.application.models.user import User

from authark.application.coordinators.auth_coordinator import AuthCoordinator
from authark.application.repositories.user_repository import (
    MemoryUserRepository)
from authark.infrastructure.crypto.pyjwt_token_service import PyJWTTokenService


RegistryConfig = Dict[str, Any]


class Registry(Dict[str, Any]):

    def __init__(self, config: RegistryConfig) -> None:

        # Services
        user_repository = MemoryUserRepository()
        token_service = PyJWTTokenService('DEVSECRET123', 'HS256')
        auth_coordinator = AuthCoordinator(user_repository, token_service)

        self['auth_coordinator'] = auth_coordinator
