from collections import UserDict
from typing import Any, Dict
from abc import ABC, abstractmethod
from authark.application.models.user import User
from authark.application.models.credential import Credential
from authark.application.coordinators.auth_coordinator import AuthCoordinator
from authark.application.reporters.authark_reporter import (
    AutharkReporter, MemoryAutharkReporter)
from authark.application.repositories.user_repository import (
    MemoryUserRepository)
from authark.application.repositories.credential_repository import (
    MemoryCredentialRepository)
from authark.application.repositories.expression_parser import ExpressionParser
from authark.application.services.token_service import MemoryTokenService
from authark.application.services.hash_service import MemoryHashService
from authark.application.services.id_service import StandardIdService
from authark.infrastructure.crypto.pyjwt_token_service import PyJWTTokenService
from authark.infrastructure.crypto.passlib_hash_service import (
    PasslibHashService)
from authark.infrastructure.data.init_json_database import init_json_database
from authark.infrastructure.data.json_user_repository import (
    JsonUserRepository)
from authark.infrastructure.data.json_credential_repository import (
    JsonCredentialRepository)
from authark.infrastructure.data.json_authark_reporter import (
    JsonAutharkReporter)
from authark.infrastructure.config.config import Config


class Registry(dict, ABC):
    @abstractmethod
    def __init__(self, config: Config) -> None:
        pass


class MemoryRegistry(Registry):

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        # Services
        parser = ExpressionParser()
        user_repository = MemoryUserRepository(parser)
        credential_repository = MemoryCredentialRepository(parser)
        hash_service = MemoryHashService()
        token_service = MemoryTokenService()
        id_service = StandardIdService()

        auth_reporter = MemoryAutharkReporter(user_repository,
                                              credential_repository)
        auth_coordinator = AuthCoordinator(
            user_repository, credential_repository,
            hash_service, token_service, id_service)

        self['auth_coordinator'] = auth_coordinator
        self['auth_reporter'] = auth_reporter


class JsonJwtRegistry(Registry):

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        database_config = config.get("database", {})
        database_path = database_config.get("url")

        # Initialize Json Database
        init_json_database(database_path)

        # Services
        parser = ExpressionParser()
        user_repository = JsonUserRepository(
            database_path, parser, 'users', User)
        credential_repository = JsonCredentialRepository(
            database_path, parser, 'credentials', Credential)
        token_service = PyJWTTokenService('DEVSECRET123', 'HS256')
        hash_service = PasslibHashService()
        id_service = StandardIdService()

        auth_reporter = JsonAutharkReporter(user_repository,
                                            credential_repository)
        auth_coordinator = AuthCoordinator(
            user_repository, credential_repository,
            hash_service, token_service, id_service)

        self['auth_coordinator'] = auth_coordinator
        self['auth_reporter'] = auth_reporter
