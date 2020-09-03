from injectark import Factory
from ..application.domain.common import (
    QueryParser, TenantProvider, StandardTenantProvider,
    AuthProvider, StandardAuthProvider)
from ..application.domain.repositories import (
    UserRepository, MemoryUserRepository,
    CredentialRepository, MemoryCredentialRepository,
    DominionRepository, MemoryDominionRepository,
    RoleRepository, MemoryRoleRepository,
    RankingRepository, MemoryRankingRepository,
    RestrictionRepository, MemoryRestrictionRepository,
    PolicyRepository, MemoryPolicyRepository)
from ..application.domain.services import (
    HashService, MemoryHashService,
    AccessTokenService, MemoryAccessTokenService,
    RefreshTokenService, MemoryRefreshTokenService,
    ImportService, MemoryImportService, AccessService)
from ..application.managers import (
    AuthManager, ManagementManager,
    ImportManager, SessionManager, SecurityManager)
from ..application.informers import (
    StandardAutharkInformer, StandardComposingInformer)
from ..core.common import Config
from ..core.suppliers import (
    TenantSupplier, MemoryTenantSupplier, MemorySetupSupplier)


class BaseFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config

    # Repositories

    def query_parser(self) -> QueryParser:
        return QueryParser()

    def standard_auth_provider(self) -> StandardAuthProvider:
        return StandardAuthProvider()

    def standard_tenant_provider(self) -> StandardTenantProvider:
        return StandardTenantProvider()

    def memory_user_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> MemoryUserRepository:
        return MemoryUserRepository(
            query_parser, tenant_provider, auth_provider)

    def memory_credential_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> MemoryCredentialRepository:
        return MemoryCredentialRepository(
            query_parser, tenant_provider, auth_provider)

    def memory_dominion_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> MemoryDominionRepository:
        return MemoryDominionRepository(
            query_parser, tenant_provider, auth_provider)

    def memory_role_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> MemoryRoleRepository:
        return MemoryRoleRepository(
            query_parser, tenant_provider, auth_provider)

    def memory_restriction_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> MemoryRestrictionRepository:
        return MemoryRestrictionRepository(
            query_parser, tenant_provider, auth_provider)

    def memory_policy_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> MemoryPolicyRepository:
        return MemoryPolicyRepository(
            query_parser, tenant_provider, auth_provider)

    def memory_ranking_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> MemoryRankingRepository:
        return MemoryRankingRepository(
            query_parser, tenant_provider, auth_provider)

    # Services

    def memory_hash_service(self) -> MemoryHashService:
        return MemoryHashService()

    def memory_access_token_service(self) -> MemoryAccessTokenService:
        return MemoryAccessTokenService()

    def memory_refresh_token_service(self) -> MemoryRefreshTokenService:
        return MemoryRefreshTokenService()

    def memory_import_service(self) -> MemoryImportService:
        return MemoryImportService()

    # Managers

    def auth_manager(
            self, user_repository: UserRepository,
            credential_repository: CredentialRepository,
            dominion_repository: DominionRepository,
            hash_service: HashService,
            access_service: AccessService,
            refresh_token_service: RefreshTokenService) -> AuthManager:
        return AuthManager(
            user_repository, credential_repository,
            dominion_repository,
            hash_service, access_service, refresh_token_service)

    def management_manager(
        self, user_repository: UserRepository,
        dominion_repository: DominionRepository,
        role_repository: RoleRepository,
        ranking_repository: RankingRepository
    ) -> ManagementManager:
        return ManagementManager(
            user_repository, dominion_repository,
            role_repository, ranking_repository)

    def import_manager(self,
                       import_service: ImportService,
                       user_repository: UserRepository,
                       credential_repository: CredentialRepository,
                       role_repository: RoleRepository,
                       ranking_repository: RankingRepository,
                       dominion_repository: DominionRepository,
                       ) -> ImportManager:
        return ImportManager(import_service, user_repository,
                             credential_repository, role_repository,
                             ranking_repository, dominion_repository)

    def session_manager(
        self, tenant_provider: TenantProvider,
        auth_provider: AuthProvider
    ) -> SessionManager:
        return SessionManager(tenant_provider, auth_provider)

    def security_manager(
        self, restriction_repository: RestrictionRepository,
        policy_repository: PolicyRepository
    ) -> SecurityManager:
        return SecurityManager(restriction_repository, policy_repository)

    def access_service(
            self, ranking_repository: RankingRepository,
            role_repository: RoleRepository,
            dominion_repository: DominionRepository,
            token_service: AccessTokenService,
            tenant_provider: TenantProvider) -> AccessService:
        return AccessService(
            ranking_repository, role_repository,
            dominion_repository,
            token_service, tenant_provider)

    # Reporters

    def standard_authark_informer(
        self, user_repository: UserRepository,
        credential_repository: CredentialRepository,
        dominion_repository: DominionRepository,
        role_repository: RoleRepository,
        restriction_repository: RestrictionRepository,
        policy_repository: PolicyRepository,
        ranking_repository: RankingRepository
    ) -> StandardAutharkInformer:
        return StandardAutharkInformer(
            user_repository, credential_repository,
            dominion_repository, role_repository,
            restriction_repository, policy_repository,
            ranking_repository)

    def standard_composing_informer(
        self, dominion_repository: DominionRepository,
        role_repository: RoleRepository,
        ranking_repository: RankingRepository
    ) -> StandardComposingInformer:
        return StandardComposingInformer(
            dominion_repository, role_repository, ranking_repository)

    # Suppliers

    def memory_tenant_supplier(self) -> TenantSupplier:
        return MemoryTenantSupplier()

    def memory_setup_supplier(self) -> MemorySetupSupplier:
        return MemorySetupSupplier()
