from ..config import Config
from ...application.models import (
    User, Credential, Dominion, Role, Ranking)
from ...application.repositories import (
    ExpressionParser,
    UserRepository, MemoryUserRepository,
    CredentialRepository, MemoryCredentialRepository,
    DominionRepository, MemoryDominionRepository,
    RoleRepository, MemoryRoleRepository,
    RankingRepository, MemoryRankingRepository)
from ...application.services import (
    HashService, MemoryHashService,
    TokenService, MemoryTokenService,
    AccessTokenService, MemoryAccessTokenService,
    RefreshTokenService, MemoryRefreshTokenService,
    AccessService, StandardAccessService, ImportService, MemoryImportService)
from ...application.coordinators import (
    AuthCoordinator, ManagementCoordinator, SetupCoordinator)
from ...application.reporters import (
    StandardAutharkReporter, StandardComposingReporter)
from .factory import Factory


class MemoryFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config

    # Repositories

    def expression_parser(self) -> ExpressionParser:
        return ExpressionParser()

    def memory_user_repository(
            self, expression_parser: ExpressionParser
    ) -> MemoryUserRepository:
        return MemoryUserRepository(expression_parser)

    def memory_credential_repository(
            self, expression_parser: ExpressionParser
    ) -> MemoryCredentialRepository:
        return MemoryCredentialRepository(expression_parser)

    def memory_dominion_repository(
            self, expression_parser: ExpressionParser
    ) -> MemoryDominionRepository:
        return MemoryDominionRepository(expression_parser)

    def memory_role_repository(
            self, expression_parser: ExpressionParser
    ) -> MemoryRoleRepository:
        return MemoryRoleRepository(expression_parser)

    def memory_ranking_repository(
            self, expression_parser: ExpressionParser
    ) -> MemoryRankingRepository:
        return MemoryRankingRepository(expression_parser)

    # Services

    def memory_hash_service(self) -> MemoryHashService:
        return MemoryHashService()

    def memory_access_token_service(self) -> MemoryAccessTokenService:
        return MemoryAccessTokenService()

    def memory_refresh_token_service(self) -> MemoryRefreshTokenService:
        return MemoryRefreshTokenService()

    def memory_import_service(self) -> MemoryImportService:
        return MemoryImportService()

    def standard_access_service(
            self, ranking_repository: RankingRepository,
            role_repository: RoleRepository,
            dominion_repository: DominionRepository,
            token_service: AccessTokenService) -> StandardAccessService:
        return StandardAccessService(
            ranking_repository, role_repository,
            dominion_repository, token_service)

    # Coordinators

    def auth_coordinator(
            self, user_repository: UserRepository,
            credential_repository: CredentialRepository,
            hash_service: HashService,
            access_service: AccessService,
            refresh_token_service: RefreshTokenService) -> AuthCoordinator:
        return AuthCoordinator(
            user_repository, credential_repository,
            hash_service, access_service, refresh_token_service)

    def management_coordinator(
        self, user_repository: UserRepository,
        dominion_repository: DominionRepository,
        role_repository: RoleRepository,
        ranking_repository: RankingRepository
    ) -> ManagementCoordinator:
        return ManagementCoordinator(
            user_repository, dominion_repository,
            role_repository, ranking_repository)

    def setup_coordinator(self,
                          import_service: ImportService,
                          user_repository: UserRepository,
                          credential_repository: CredentialRepository,
                          role_repository: RoleRepository,
                          ranking_repository: RankingRepository,
                          dominion_repository: DominionRepository,
                          ) -> SetupCoordinator:
        return SetupCoordinator(import_service, user_repository,
                                credential_repository, role_repository,
                                ranking_repository, dominion_repository)

    # Reporters

    def standard_authark_reporter(
        self, user_repository: UserRepository,
        credential_repository: CredentialRepository,
        dominion_repository: DominionRepository,
        role_repository: RoleRepository
    ) -> StandardAutharkReporter:
        return StandardAutharkReporter(
            user_repository, credential_repository,
            dominion_repository, role_repository)

    def standard_composing_reporter(
        self, user_repository: UserRepository,
        dominion_repository: DominionRepository,
        role_repository: RoleRepository,
        ranking_repository: RankingRepository
    ) -> StandardComposingReporter:
        return StandardComposingReporter(
            user_repository, dominion_repository,
            role_repository, ranking_repository)
