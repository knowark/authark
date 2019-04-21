from ..config import Config
from ...application.utilities import ExpressionParser
from ...application.repositories import (
    UserRepository, MemoryUserRepository,
    CredentialRepository, MemoryCredentialRepository,
    DominionRepository, MemoryDominionRepository,
    RoleRepository, MemoryRoleRepository,
    RankingRepository, MemoryRankingRepository,
    PolicyRepository, MemoryPolicyRepository,
    ResourceRepository, MemoryResourceRepository,
    PermissionRepository, MemoryPermissionRepository,
    GrantRepository, MemoryGrantRepository)
from ...application.services import (
    HashService, MemoryHashService,
    TokenService, MemoryTokenService,
    AccessTokenService, MemoryAccessTokenService,
    RefreshTokenService, MemoryRefreshTokenService,
    ImportService, MemoryImportService,
    CatalogService, MemoryCatalogService,
    ProvisionService, MemoryProvisionService,
    TenantService, StandardTenantService,
    ExportService, MemoryExportService)
from ...application.coordinators import (
    AuthCoordinator, ManagementCoordinator,
    ImportCoordinator, SetupCoordinator, AssignmentCoordinator,
    AffiliationCoordinator, AccessCoordinator, ExportCoordinator)
from ...application.reporters import (
    StandardAutharkReporter, StandardComposingReporter,
    StandardTenancyReporter)
from .factory import Factory


class MemoryFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config

    # Repositories

    def expression_parser(self) -> ExpressionParser:
        return ExpressionParser()

    def memory_user_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> MemoryUserRepository:
        return MemoryUserRepository(expression_parser, tenant_service)

    def memory_credential_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> MemoryCredentialRepository:
        return MemoryCredentialRepository(expression_parser, tenant_service)

    def memory_dominion_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> MemoryDominionRepository:
        return MemoryDominionRepository(expression_parser, tenant_service)

    def memory_role_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> MemoryRoleRepository:
        return MemoryRoleRepository(expression_parser, tenant_service)

    def memory_ranking_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> MemoryRankingRepository:
        return MemoryRankingRepository(expression_parser, tenant_service)

    def memory_policy_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> MemoryPolicyRepository:
        return MemoryPolicyRepository(expression_parser, tenant_service)

    def memory_resource_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> MemoryResourceRepository:
        return MemoryResourceRepository(expression_parser, tenant_service)

    def memory_permission_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> MemoryPermissionRepository:
        return MemoryPermissionRepository(expression_parser, tenant_service)

    def memory_grant_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> MemoryGrantRepository:
        return MemoryGrantRepository(expression_parser, tenant_service)

    # Services

    def memory_hash_service(self) -> MemoryHashService:
        return MemoryHashService()

    def memory_access_token_service(self) -> MemoryAccessTokenService:
        return MemoryAccessTokenService()

    def memory_refresh_token_service(self) -> MemoryRefreshTokenService:
        return MemoryRefreshTokenService()

    def memory_import_service(self) -> MemoryImportService:
        return MemoryImportService()

    def memory_export_service(self) -> MemoryExportService:
        return MemoryExportService()

    def memory_catalog_service(
            self, expression_parser: ExpressionParser
    ) -> MemoryCatalogService:
        return MemoryCatalogService(expression_parser)

    def memory_provision_service(self) -> MemoryProvisionService:
        return MemoryProvisionService()

    def standard_tenant_service(self) -> StandardTenantService:
        return StandardTenantService()

    # Coordinators

    def auth_coordinator(
            self, user_repository: UserRepository,
            credential_repository: CredentialRepository,
            hash_service: HashService,
            access_coordinator: AccessCoordinator,
            refresh_token_service: RefreshTokenService) -> AuthCoordinator:
        return AuthCoordinator(
            user_repository, credential_repository,
            hash_service, access_coordinator, refresh_token_service)

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

    def export_coordinator(self,
                           export_service: ExportService,
                           catalog_service: CatalogService
                           ) -> ExportCoordinator:
        return ExportCoordinator(export_service, catalog_service)

    def setup_coordinator(self,
                          catalog_service: CatalogService,
                          provision_service: ProvisionService,
                          token_service: TokenService
                          ) -> SetupCoordinator:
        return SetupCoordinator(catalog_service, provision_service,
                                token_service)

    def assignment_coordinator(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        ranking_repository: RankingRepository,
        policy_repository: PolicyRepository,
        resource_repository: ResourceRepository,
        permission_repository: PermissionRepository,
        grant_repository: GrantRepository
    ) -> AssignmentCoordinator:
        return AssignmentCoordinator(
            user_repository, role_repository, ranking_repository,
            policy_repository, resource_repository, permission_repository,
            grant_repository)

    def affiliation_coordinator(
        self, catalog_service: CatalogService,
        tenant_service: TenantService,
    ) -> AffiliationCoordinator:
        return AffiliationCoordinator(catalog_service, tenant_service)

    def access_coordinator(
            self, ranking_repository: RankingRepository,
            role_repository: RoleRepository,
            dominion_repository: DominionRepository,
            resource_repository: ResourceRepository,
            grant_repository: GrantRepository,
            permission_repository: PermissionRepository,
            policy_repository: PolicyRepository,
            token_service: AccessTokenService,
            tenant_service: TenantService) -> AccessCoordinator:
        return AccessCoordinator(
            ranking_repository, role_repository,
            dominion_repository, resource_repository, grant_repository,
            permission_repository, policy_repository, token_service,
            tenant_service)

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
        policy_repository: PolicyRepository,
        permission_repository: PermissionRepository,
        grant_repository: GrantRepository
    ) -> StandardComposingReporter:
        return StandardComposingReporter(
            dominion_repository, role_repository, ranking_repository,
            resource_repository, policy_repository, permission_repository,
            grant_repository)

    def standard_tenancy_reporter(
        self, catalog_service: CatalogService
    ) -> StandardTenancyReporter:
        return StandardTenancyReporter(catalog_service)
