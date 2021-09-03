from injectark import Factory
from ...application.domain.common import (
    QueryParser, AuthProvider, StandardAuthProvider)
from ...application.domain.services.repositories import (
    UserRepository, MemoryUserRepository,
    CredentialRepository, MemoryCredentialRepository,
    DominionRepository, MemoryDominionRepository,
    RoleRepository, MemoryRoleRepository,
    RankingRepository, MemoryRankingRepository,
    RestrictionRepository, MemoryRestrictionRepository,
    PolicyRepository, MemoryPolicyRepository)
from ...application.domain.services import (
    HashService, MemoryHashService,
    AccessTokenService, MemoryAccessTokenService,
    RefreshTokenService, MemoryRefreshTokenService,
    VerificationTokenService, MemoryVerificationTokenService,
    ImportService, MemoryImportService, EnrollmentService,
    AccessService, VerificationService, IdentityService,
    MemoryIdentityService)
from ...application.general.suppliers import (
    TenantSupplier, MemoryTenantSupplier,
    SetupSupplier, MemorySetupSupplier)
from ...application.operation.managers import (
    AuthManager, ManagementManager, ImportManager,
    SessionManager, SecurityManager, ProcedureManager,
    TenantManager, SetupManager)
from ...application.operation.informers import (
    StandardInformer, ComposingInformer, TenantInformer)
from ...application.general import (
    PlanSupplier, MemoryPlanSupplier)
from ..core.common import Config
from ..core.suppliers import (
    TemplateSupplier, MemoryTemplateSupplier)


class BaseFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.public = [
            'StandardInformer', 'ComposingInformer', 'TenantInformer',
            'AuthManager', 'ImportManager', 'ManagementManager',
            'TenantManager', 'ProcedureManager', 'SecurityManager',
            'SetupManager', 'SessionManager'
        ]


    # Repositories

    def query_parser(self) -> QueryParser:
        return QueryParser()

    def auth_provider(self) -> AuthProvider:
        return StandardAuthProvider()

    def user_repository(
        self, query_parser: QueryParser,
        auth_provider: AuthProvider
    ) -> UserRepository:
        return MemoryUserRepository(
            query_parser, auth_provider, auth_provider)

    def credential_repository(
        self, query_parser: QueryParser,
        auth_provider: AuthProvider
    ) -> CredentialRepository:
        return MemoryCredentialRepository(
            query_parser, auth_provider, auth_provider)

    def dominion_repository(
        self, query_parser: QueryParser,
        auth_provider: AuthProvider
    ) -> DominionRepository:
        return MemoryDominionRepository(
            query_parser, auth_provider, auth_provider)

    def role_repository(
        self, query_parser: QueryParser,
        auth_provider: AuthProvider
    ) -> RoleRepository:
        return MemoryRoleRepository(
            query_parser, auth_provider, auth_provider)

    def restriction_repository(
        self, query_parser: QueryParser,
        auth_provider: AuthProvider
    ) -> RestrictionRepository:
        return MemoryRestrictionRepository(
            query_parser, auth_provider, auth_provider)

    def policy_repository(
        self, query_parser: QueryParser,
        auth_provider: AuthProvider
    ) -> PolicyRepository:
        return MemoryPolicyRepository(
            query_parser, auth_provider, auth_provider)

    def ranking_repository(
        self, query_parser: QueryParser,
        auth_provider: AuthProvider
    ) -> RankingRepository:
        return MemoryRankingRepository(
            query_parser, auth_provider, auth_provider)

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

    def identity_service(self) -> IdentityService:
        return MemoryIdentityService()

    def access_service(
        self, ranking_repository: RankingRepository,
        role_repository: RoleRepository,
        dominion_repository: DominionRepository,
        token_service: AccessTokenService
    ) -> AccessService:
        return AccessService(
            ranking_repository, role_repository,
            dominion_repository, token_service)

    def verification_service(
        self, user_repository: UserRepository,
        token_service: VerificationTokenService
    ) -> VerificationService:
        return VerificationService(
            user_repository, token_service)

    def enrollment_service(
        self, user_repository: UserRepository,
        credential_repository: CredentialRepository,
        hash_service: HashService,
        token_service: VerificationTokenService,
    ) -> EnrollmentService:
        return EnrollmentService(
            user_repository, credential_repository, hash_service )

    # Suppliers

    def plan_supplier(self) -> PlanSupplier:
        return MemoryPlanSupplier()

    # Managers

    def auth_manager(
        self, auth_provider: AuthProvider,
        user_repository: UserRepository,
        credential_repository: CredentialRepository,
        dominion_repository: DominionRepository,
        hash_service: HashService,
        access_service: AccessService,
        refresh_token_service: RefreshTokenService,
        identity_service: IdentityService,
        tenant_supplier: TenantSupplier
    ) -> AuthManager:
        return AuthManager(
            auth_provider, user_repository, credential_repository,
            dominion_repository, hash_service, access_service,
            refresh_token_service, identity_service,
            tenant_supplier)

    def management_manager(
        self, user_repository: UserRepository,
        dominion_repository: DominionRepository,
        role_repository: RoleRepository,
        ranking_repository: RankingRepository
    ) -> ManagementManager:
        return ManagementManager(
            user_repository, dominion_repository,
            role_repository, ranking_repository)

    def import_manager(
        self,
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
        self, auth_provider: AuthProvider
    ) -> SessionManager:
        return SessionManager(auth_provider)

    def security_manager(
        self, restriction_repository: RestrictionRepository,
        policy_repository: PolicyRepository
    ) -> SecurityManager:
        return SecurityManager(restriction_repository, policy_repository)

    def procedure_manager(
        self,  auth_provider: AuthProvider,
        user_repository: UserRepository,
        enrollment_service: EnrollmentService,
        verification_service: VerificationService,
        identity_service: IdentityService,
        plan_supplier: PlanSupplier,
        tenant_supplier: TenantSupplier,
    ) -> ProcedureManager:
        return ProcedureManager(
            auth_provider, user_repository, enrollment_service,
            verification_service, identity_service, plan_supplier,
            tenant_supplier)

    def tenant_manager(
        self, tenant_supplier: TenantSupplier
    ) -> TenantManager:
        return TenantManager(tenant_supplier)

    def setup_manager(
        self, setup_supplier: SetupSupplier
    ) -> SetupManager:
        return SetupManager(setup_supplier)

    # Reporters

    def standard_informer(
        self, user_repository: UserRepository,
        credential_repository: CredentialRepository,
        dominion_repository: DominionRepository,
        role_repository: RoleRepository,
        restriction_repository: RestrictionRepository,
        policy_repository: PolicyRepository,
        ranking_repository: RankingRepository
    ) -> StandardInformer:
        return StandardInformer(
            user_repository, credential_repository,
            dominion_repository, role_repository,
            restriction_repository, policy_repository,
            ranking_repository)

    def composing_informer(
        self, dominion_repository: DominionRepository,
        role_repository: RoleRepository,
        ranking_repository: RankingRepository
    ) -> ComposingInformer:
        return ComposingInformer(
            dominion_repository, role_repository, ranking_repository)

    def tenant_informer(
        self, tenant_supplier: TenantSupplier,
    ) -> TenantInformer:
        return TenantInformer(tenant_supplier)

    # Suppliers

    def tenant_supplier(self) -> TenantSupplier:
        return MemoryTenantSupplier()

    def setup_supplier(self) -> SetupSupplier:
        return MemorySetupSupplier()

    def template_supplier(self) -> TemplateSupplier:
        return MemoryTemplateSupplier()
