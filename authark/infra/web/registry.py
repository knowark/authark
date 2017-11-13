from collections import UserDict
from typing import Any, Dict
from authark.app.models.user import User

from authark.app.coordinators.auth_coordinator import AuthCoordinator
from authark.infra.db.memory_user_repository import MemoryUserRepository
from authark.infra.crypto.pyjwt_token_service import PyJWTTokenService


class Registry(Dict[str, Any]):

    def __init__(self) -> None:

        # Services
        user_repository = MemoryUserRepository()
        token_service = PyJWTTokenService('DEVSECRET123', 'HS256')
        auth_coordinator = AuthCoordinator(user_repository, token_service)

        self['auth_coordinator'] = auth_coordinator
