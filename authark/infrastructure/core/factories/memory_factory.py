from ....application.utilities import (
    ExpressionParser, TenantProvider, StandardTenantProvider)
from ....application.repositories import (
    UserRepository, MemoryUserRepository,
    CredentialRepository, MemoryCredentialRepository,
    DominionRepository, MemoryDominionRepository,
    RoleRepository, MemoryRoleRepository,
    RankingRepository, MemoryRankingRepository,
    PolicyRepository, MemoryPolicyRepository,
    ResourceRepository, MemoryResourceRepository)
from ....application.services import (
    HashService, MemoryHashService,
    TokenService, MemoryTokenService,
    AccessTokenService, MemoryAccessTokenService,
    RefreshTokenService, MemoryRefreshTokenService,
    ImportService, MemoryImportService, AccessService)
from ....application.coordinators import (
    AuthCoordinator, ManagementCoordinator,
    ImportCoordinator, SessionCoordinator)
from ....application.reporters import (
    StandardAutharkReporter, StandardComposingReporter)
from ..configuration import Config
from ..tenancy import TenantSupplier, MemoryTenantSupplier
from .factory import Factory


class MemoryFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config

    # Repositories

    def expression_parser(self) -> ExpressionParser:
        return ExpressionParser()

    def memory_user_repository(
            self, expression_parser: ExpressionParser,
            tenant_provider: TenantProvider
    ) -> MemoryUserRepository:
        return MemoryUserRepository(expression_parser, tenant_provider)

    def memory_credential_repository(
            self, expression_parser: ExpressionParser,
            tenant_provider: TenantProvider
    ) -> MemoryCredentialRepository:
        return MemoryCredentialRepository(expression_parser, tenant_provider)

    def memory_dominion_repository(
            self, expression_parser: ExpressionParser,
            tenant_provider: TenantProvider
    ) -> MemoryDominionRepository:
        return MemoryDominionRepository(expression_parser, tenant_provider)

    def memory_role_repository(
            self, expression_parser: ExpressionParser,
            tenant_provider: TenantProvider
    ) -> MemoryRoleRepository:
        return MemoryRoleRepository(expression_parser, tenant_provider)

    def memory_ranking_repository(
            self, expression_parser: ExpressionParser,
            tenant_provider: TenantProvider
    ) -> MemoryRankingRepository:
        return MemoryRankingRepository(expression_parser, tenant_provider)

    def memory_policy_repository(
            self, expression_parser: ExpressionParser,
            tenant_provider: TenantProvider
    ) -> MemoryPolicyRepository:
        return MemoryPolicyRepository(expression_parser, tenant_provider)

    def memory_resource_repository(
            self, expression_parser: ExpressionParser,
            tenant_provider: TenantProvider
    ) -> MemoryResourceRepository:
        return MemoryResourceRepository(expression_parser, tenant_provider)

    # Services

    def memory_hash_service(self) -> MemoryHashService:
        return MemoryHashService()

    def memory_access_token_service(self) -> MemoryAccessTokenService:
        return MemoryAccessTokenService()

    def memory_refresh_token_service(self) -> MemoryRefreshTokenService:
        return MemoryRefreshTokenService()

    def memory_import_service(self) -> MemoryImportService:
        return MemoryImportService()

    def standard_tenant_provider(self) -> StandardTenantProvider:
        return StandardTenantProvider()

    # Coordinators

    def auth_coordinator(
            self, user_repository: UserRepository,
            credential_repository: CredentialRepository,
            dominion_repository: DominionRepository,
            hash_service: HashService,
            access_service: AccessService,
            refresh_token_service: RefreshTokenService) -> AuthCoordinator:
        return AuthCoordinator(
            user_repository, credential_repository,
            dominion_repository,
            hash_service, access_service, refresh_token_service)

    def management_coordinator(
        self, user_repository: UserRepository,
        dominion_repository: DominionRepository,
        role_repository: RoleRepository,
        ranking_repository: RankingRepository,
        policy_repository: PolicyRepository,
        resource_repository: ResourceRepository
    ) -> ManagementCoordinator:
        return ManagementCoordinator(
            user_repository, dominion_repository,
            role_repository, ranking_repository, policy_repository,
            resource_repository)

    def import_coordinator(self,
                           import_service: ImportService,
                           user_repository: UserRepository,
                           credential_repository: CredentialRepository,
                           role_repository: RoleRepository,
                           ranking_repository: RankingRepository,
                           dominion_repository: DominionRepository,
                           ) -> ImportCoordinator:
        return ImportCoordinator(import_service, user_repository,
                                 credential_repository, role_repository,
                                 ranking_repository, dominion_repository)

    def session_coordinator(
        self, tenant_provider: TenantProvider
    ) -> SessionCoordinator:
        return SessionCoordinator(tenant_provider)

    def access_service(
            self, ranking_repository: RankingRepository,
            role_repository: RoleRepository,
            dominion_repository: DominionRepository,
            resource_repository: ResourceRepository,
            policy_repository: PolicyRepository,
            token_service: AccessTokenService,
            tenant_provider: TenantProvider) -> AccessService:
        return AccessService(
            ranking_repository, role_repository,
            dominion_repository, resource_repository,
            policy_repository, token_service, tenant_provider)

    # Reporters

    def standard_authark_reporter(
        self, user_repository: UserRepository,
        credential_repository: CredentialRepository,
        dominion_repository: DominionRepository,
        role_repository: RoleRepository,
        policy_repository: PolicyRepository,
        resource_repository: ResourceRepository
    ) -> StandardAutharkReporter:
        return StandardAutharkReporter(
            user_repository, credential_repository,
            dominion_repository, role_repository,
            policy_repository, resource_repository)

    def standard_composing_reporter(
        self, dominion_repository: DominionRepository,
        role_repository: RoleRepository,
        ranking_repository: RankingRepository,
        resource_repository: ResourceRepository,
        policy_repository: PolicyRepository
    ) -> StandardComposingReporter:
        return StandardComposingReporter(
            dominion_repository, role_repository, ranking_repository,
            resource_repository, policy_repository)

    def memory_tenant_supplier(self) -> TenantSupplier:
        return MemoryTenantSupplier()
