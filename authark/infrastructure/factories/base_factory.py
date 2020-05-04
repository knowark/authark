from injectark import Factory
from ...application.utilities import (
    QueryParser, TenantProvider, StandardTenantProvider)
from ...application.repositories import (
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
    ImportService, MemoryImportService, AccessService)
from ...application.coordinators import (
    AuthCoordinator, ManagementCoordinator,
    ImportCoordinator, SessionCoordinator)
from ...application.informers import (
    StandardAutharkInformer, StandardComposingInformer)
from ..config import Config, config
from ..core.tenancy import TenantSupplier, MemoryTenantSupplier
from ..web import WebApplication


class BaseFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config

    # Repositories

    def query_parser(self) -> QueryParser:
        return QueryParser()

    def memory_user_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
    ) -> MemoryUserRepository:
        return MemoryUserRepository(query_parser, tenant_provider)

    def memory_credential_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
    ) -> MemoryCredentialRepository:
        return MemoryCredentialRepository(query_parser, tenant_provider)

    def memory_dominion_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
    ) -> MemoryDominionRepository:
        return MemoryDominionRepository(query_parser, tenant_provider)

    def memory_role_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
    ) -> MemoryRoleRepository:
        return MemoryRoleRepository(query_parser, tenant_provider)

    def memory_ranking_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
    ) -> MemoryRankingRepository:
        return MemoryRankingRepository(query_parser, tenant_provider)

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
        ranking_repository: RankingRepository
    ) -> ManagementCoordinator:
        return ManagementCoordinator(
            user_repository, dominion_repository,
            role_repository, ranking_repository)

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
        self, tenant_provider: TenantProvider,
        auth_provider: AuthProvider
    ) -> SessionCoordinator:
        return SessionCoordinator(tenant_provider, auth_provider)

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

    def standard_authark_reporter(
        self, user_repository: UserRepository,
        credential_repository: CredentialRepository,
        dominion_repository: DominionRepository,
        role_repository: RoleRepository,
    ) -> StandardAutharkInformer:
        return StandardAutharkInformer(
            user_repository, credential_repository,
            dominion_repository, role_repository)

    def standard_composing_reporter(
        self, dominion_repository: DominionRepository,
        role_repository: RoleRepository,
        ranking_repository: RankingRepository
    ) -> StandardComposingInformer:
        return StandardComposingInformer(
            dominion_repository, role_repository, ranking_repository)

    def memory_tenant_supplier(self) -> TenantSupplier:
        return MemoryTenantSupplier()

    # Presentation

    def web_application(self) -> WebApplication:
        return WebApplication(self.config, self.injector)
