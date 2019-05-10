from ....application.services import TenantService
from ....application.utilities import ExpressionParser
from ....application.repositories import UserRepository
from ....application.services import HashService, TokenService
from ...data import (
    JsonCredentialRepository,
    JsonDominionRepository, JsonRoleRepository,
    JsonRepository, JsonUserRepository,
    JsonRankingRepository, JsonImportService,
    JsonPolicyRepository, JsonResourceRepository,
    JsonGrantRepository, JsonPermissionRepository)
from ..configuration import Config
from ..tenancy import TenantSupplier
from .crypto_factory import CryptoFactory


class JsonFactory(CryptoFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.path = self.config['data']['json']['default']

    # Repositories

    def json_user_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> JsonUserRepository:
        return JsonUserRepository(self.path, expression_parser,
                                  tenant_service)

    def json_credential_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> JsonCredentialRepository:
        return JsonCredentialRepository(self.path, expression_parser,
                                        tenant_service)

    def json_dominion_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> JsonDominionRepository:
        return JsonDominionRepository(self.path, expression_parser,
                                      tenant_service)

    def json_role_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> JsonRoleRepository:
        return JsonRoleRepository(self.path, expression_parser,
                                  tenant_service)

    def json_ranking_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> JsonRankingRepository:
        return JsonRankingRepository(self.path, expression_parser,
                                     tenant_service)

    def json_policy_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> JsonPolicyRepository:
        return JsonPolicyRepository(self.path, expression_parser,
                                    tenant_service)

    def json_resource_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> JsonResourceRepository:
        return JsonResourceRepository(self.path, expression_parser,
                                      tenant_service)

    def json_grant_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> JsonGrantRepository:
        return JsonGrantRepository(self.path, expression_parser,
                                   tenant_service)

    def json_permission_repository(
            self, expression_parser: ExpressionParser,
            tenant_service: TenantService
    ) -> JsonPermissionRepository:
        return JsonPermissionRepository(self.path, expression_parser,
                                        tenant_service)

    def json_import_service(
            self, hash_service: HashService) -> JsonImportService:
        return JsonImportService(hash_service)

    def tenant_supplier(self) -> TenantSupplier:
        catalog_path = self.config['tenancy']['json']
        directory_data = self.config['data']['json']['default']
        return TenantSupplier(catalog_path, directory_data)
