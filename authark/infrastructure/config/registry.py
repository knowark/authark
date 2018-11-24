from collections import UserDict
from typing import Any, Dict
from abc import ABC, abstractmethod
from ...application.models import (
    User, Credential, Dominion)
from ...application.repositories import (
    ExpressionParser,
    UserRepository, MemoryUserRepository,
    CredentialRepository, MemoryCredentialRepository,
    DominionRepository, MemoryDominionRepository,
    RoleRepository, MemoryRoleRepository,
    RankingRepository, MemoryRankingRepository)
from ...application.services import (
    MemoryTokenService, MemoryHashService)
from ...application.coordinators import (
    AuthCoordinator, ManagementCoordinator)
from authark.application.reporters import (
    AutharkReporter, StandardAutharkReporter)
from ..crypto.pyjwt_token_service import PyJWTTokenService
from ..crypto.passlib_hash_service import (
    PasslibHashService)
from ..data import (
    init_json_database, JsonUserRepository, JsonCredentialRepository,
    JsonDominionRepository, JsonRoleRepository, JsonRankingRepository)
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
        role_repository = MemoryRoleRepository(parser)
        dominion_repository = MemoryDominionRepository(parser)
        role_repository = MemoryRoleRepository(parser)
        ranking_repository = MemoryRankingRepository(parser)
        hash_service = MemoryHashService()
        access_token_service = MemoryTokenService()
        refresh_token_service = MemoryTokenService()

        auth_reporter = StandardAutharkReporter(
            user_repository,
            credential_repository,
            dominion_repository,
            role_repository)
        auth_coordinator = AuthCoordinator(
            user_repository, credential_repository,
            hash_service, access_token_service,
            refresh_token_service)
        management_coordinator = ManagementCoordinator(
            user_repository, dominion_repository,
            role_repository, ranking_repository)

        self['auth_coordinator'] = auth_coordinator
        self['management_coordinator'] = management_coordinator
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
            database_path, parser)
        credential_repository = JsonCredentialRepository(
            database_path, parser)
        dominion_repository = JsonDominionRepository(
            database_path, parser)
        role_repository = JsonRoleRepository(
            database_path, parser)
        ranking_repository = JsonRankingRepository(
            database_path, parser)
        tokens_config = config.get("tokens", {})
        access_token_service = PyJWTTokenService(
            'DEVSECRET123', 'HS256', tokens_config.get('access_lifetime'))
        refresh_token_service = PyJWTTokenService(
            'DEVSECRET123', 'HS256', tokens_config.get('refresh_lifetime'),
            tokens_config.get('refresh_threshold'))
        hash_service = PasslibHashService()

        auth_reporter = StandardAutharkReporter(
            user_repository,
            credential_repository,
            dominion_repository,
            role_repository)
        auth_coordinator = AuthCoordinator(
            user_repository, credential_repository,
            hash_service, access_token_service,
            refresh_token_service)
        management_coordinator = ManagementCoordinator(
            user_repository, dominion_repository,
            role_repository, ranking_repository)

        self['auth_coordinator'] = auth_coordinator
        self['management_coordinator'] = management_coordinator
        self['auth_reporter'] = auth_reporter
