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
    VerificationTokenService, MemoryVerificationTokenService,
    NotificationService, MemoryNotificationService,
    ImportService, MemoryImportService, AccessService)
from ..application.managers import (
    AuthManager, ManagementManager,
    ImportManager, SessionManager, SecurityManager)
from ..application.informers import (
    AutharkInformer, StandardAutharkInformer,
    ComposingInformer, StandardComposingInformer)
from ..core.common import Config
from ..core.suppliers import (
    TenantSupplier, MemoryTenantSupplier,
    SetupSupplier, MemorySetupSupplier,
    TemplateSupplier, MemoryTemplateSupplier)


class BaseFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config

    # Repositories

    def query_parser(self) -> QueryParser:
        return QueryParser()

    def auth_provider(self) -> AuthProvider:
        return StandardAuthProvider()

    def tenant_provider(self) -> TenantProvider:
        return StandardTenantProvider()

    def user_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> UserRepository:
        return MemoryUserRepository(
            query_parser, tenant_provider, auth_provider)

    def credential_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> CredentialRepository:
        return MemoryCredentialRepository(
            query_parser, tenant_provider, auth_provider)

    def dominion_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> DominionRepository:
        return MemoryDominionRepository(
            query_parser, tenant_provider, auth_provider)

    def role_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> RoleRepository:
        return MemoryRoleRepository(
            query_parser, tenant_provider, auth_provider)

    def restriction_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> RestrictionRepository:
        return MemoryRestrictionRepository(
            query_parser, tenant_provider, auth_provider)

    def policy_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> PolicyRepository:
        return MemoryPolicyRepository(
            query_parser, tenant_provider, auth_provider)

    def ranking_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> RankingRepository:
        return MemoryRankingRepository(
            query_parser, tenant_provider, auth_provider)

    # Services

    def hash_service(self) -> HashService:
        return MemoryHashService()

    def access_token_service(self) -> AccessTokenService:
        return MemoryAccessTokenService()

    def refresh_token_service(self) -> RefreshTokenService:
        return MemoryRefreshTokenService()

    def verification_token_service(self) -> VerificationTokenService:
        return MemoryVerificationTokenService()

    def import_service(self, hash_service: HashService) -> ImportService:
        return MemoryImportService()

    def notification_service(
        self, template_supplier: TemplateSupplier) -> NotificationService:
        return MemoryNotificationService()

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

    # Managers

    def auth_manager(
            self, user_repository: UserRepository,
            credential_repository: CredentialRepository,
            dominion_repository: DominionRepository,
            hash_service: HashService,
            access_service: AccessService,
            notification_service: NotificationService,
            refresh_token_service: RefreshTokenService,
            verification_token_service: VerificationTokenService
    ) -> AuthManager:
        return AuthManager(
            user_repository, credential_repository,
            dominion_repository, hash_service, access_service,
            notification_service, refresh_token_service,
            verification_token_service)

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

    # Reporters

    def authark_informer(
        self, user_repository: UserRepository,
        credential_repository: CredentialRepository,
        dominion_repository: DominionRepository,
        role_repository: RoleRepository,
        restriction_repository: RestrictionRepository,
        policy_repository: PolicyRepository,
        ranking_repository: RankingRepository) -> AutharkInformer:
        return StandardAutharkInformer(
            user_repository, credential_repository,
            dominion_repository, role_repository,
            restriction_repository, policy_repository,
            ranking_repository)

    def composing_informer(
        self, dominion_repository: DominionRepository,
        role_repository: RoleRepository,
        ranking_repository: RankingRepository) -> ComposingInformer:
        return StandardComposingInformer(
            dominion_repository, role_repository, ranking_repository)

    # Suppliers

    def tenant_supplier(self) -> TenantSupplier:
        return MemoryTenantSupplier()

    def setup_supplier(self) -> SetupSupplier:
        return MemorySetupSupplier()

    def template_supplier(self) -> TemplateSupplier:
        return MemoryTemplateSupplier()
