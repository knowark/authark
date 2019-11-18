from ....application.utilities import ExpressionParser, TenantProvider
from ....application.repositories import UserRepository
from ....application.services import HashService, TokenService
from ...data import (
    JsonCredentialRepository,
    JsonDominionRepository, JsonRoleRepository,
    JsonRepository, JsonUserRepository,
    JsonRankingRepository, JsonImportService,
    JsonPolicyRepository, JsonResourceRepository)
from ..configuration import Config
from ..tenancy import TenantSupplier, JsonTenantSupplier
from .crypto_factory import CryptoFactory


class JsonFactory(CryptoFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.path = self.config['data']['json']['default']

    # Repositories

    def json_user_repository(
            self, expression_parser: ExpressionParser,
            tenant_provider: TenantProvider
    ) -> JsonUserRepository:
        return JsonUserRepository(self.path, expression_parser,
                                  tenant_provider)

    def json_credential_repository(
            self, expression_parser: ExpressionParser,
            tenant_provider: TenantProvider
    ) -> JsonCredentialRepository:
        return JsonCredentialRepository(self.path, expression_parser,
                                        tenant_provider)

    def json_dominion_repository(
            self, expression_parser: ExpressionParser,
            tenant_provider: TenantProvider
    ) -> JsonDominionRepository:
        return JsonDominionRepository(self.path, expression_parser,
                                      tenant_provider)

    def json_role_repository(
            self, expression_parser: ExpressionParser,
            tenant_provider: TenantProvider
    ) -> JsonRoleRepository:
        return JsonRoleRepository(self.path, expression_parser,
                                  tenant_provider)

    def json_ranking_repository(
            self, expression_parser: ExpressionParser,
            tenant_provider: TenantProvider
    ) -> JsonRankingRepository:
        return JsonRankingRepository(self.path, expression_parser,
                                     tenant_provider)

    def json_policy_repository(
            self, expression_parser: ExpressionParser,
            tenant_provider: TenantProvider
    ) -> JsonPolicyRepository:
        return JsonPolicyRepository(self.path, expression_parser,
                                    tenant_provider)

    def json_resource_repository(
            self, expression_parser: ExpressionParser,
            tenant_provider: TenantProvider
    ) -> JsonResourceRepository:
        return JsonResourceRepository(self.path, expression_parser,
                                      tenant_provider)

    def json_import_service(
            self, hash_service: HashService) -> JsonImportService:
        return JsonImportService(hash_service)

    def json_tenant_supplier(self) -> TenantSupplier:
        catalog_path = self.config['tenancy']['json']
        directory_data = self.config['data']['json']['default']
        return JsonTenantSupplier(catalog_path, directory_data)
