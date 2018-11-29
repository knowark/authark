from ...config import Config
from ....application.models import (
    User, Credential, Dominion, Role, Ranking)
from ....application.repositories import (
    ExpressionParser,
    UserRepository, MemoryUserRepository,
    CredentialRepository, MemoryCredentialRepository,
    DominionRepository, MemoryDominionRepository,
    RoleRepository, MemoryRoleRepository,
    RankingRepository, MemoryRankingRepository)
from ....application.services import (
    HashService, MemoryHashService,
    TokenService, MemoryTokenService,
    AccessService, StandardAccessService)
from ....application.coordinators import (
    AuthCoordinator, ManagementCoordinator)
from ....application.reporters import (
    StandardAutharkReporter, StandardComposingReporter)


class MemoryFactory:
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

    def standard_hash_service(self) -> MemoryHashService:
        return MemoryHashService()

    def memory_token_service(self) -> MemoryTokenService:
        return MemoryTokenService()

    def standard_access_service(
            self, ranking_repository: RankingRepository,
            role_repository: RoleRepository,
            dominion_repository: DominionRepository,
            token_service: TokenService) -> StandardAccessService:
        return StandardAccessService(
            ranking_repository, role_repository,
            dominion_repository, token_service)

    # Coordinators

    def auth_coordinator(
            self, user_repository: UserRepository,
            credential_repository: CredentialRepository,
            hash_service: HashService,
            access_service: AccessService,
            refresh_token_service: TokenService) -> AuthCoordinator:
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
