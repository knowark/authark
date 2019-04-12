from ...application.utilities import ExpressionParser
from ...application.repositories import UserRepository
from ..config import Config
from ..data import (
    init_json_database, JsonCredentialRepository,
    JsonDominionRepository, JsonRoleRepository,
    JsonRepository, JsonUserRepository,
    JsonRankingRepository, JsonImportService,
    JsonPolicyRepository, JsonResourceRepository,
    JsonGrantRepository, JsonPermissionRepository,
    JsonCatalogService, JsonProvisionService)
from .crypto_factory import CryptoFactory
from ...application.services import HashService


class JsonFactory(CryptoFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.path = self.config.get('database', {}).get('url')

    # Repositories

    def json_user_repository(
            self, expression_parser: ExpressionParser
    ) -> JsonUserRepository:
        return JsonUserRepository(self.path, expression_parser)

    def json_credential_repository(
            self, expression_parser: ExpressionParser
    ) -> JsonCredentialRepository:
        return JsonCredentialRepository(self.path, expression_parser)

    def json_dominion_repository(
            self, expression_parser: ExpressionParser
    ) -> JsonDominionRepository:
        return JsonDominionRepository(self.path, expression_parser)

    def json_role_repository(
            self, expression_parser: ExpressionParser
    ) -> JsonRoleRepository:
        return JsonRoleRepository(self.path, expression_parser)

    def json_ranking_repository(
            self, expression_parser: ExpressionParser
    ) -> JsonRankingRepository:
        return JsonRankingRepository(self.path, expression_parser)

    def json_policy_repository(
            self, expression_parser: ExpressionParser
    ) -> JsonPolicyRepository:
        return JsonPolicyRepository(self.path, expression_parser)

    def json_resource_repository(
            self, expression_parser: ExpressionParser
    ) -> JsonResourceRepository:
        return JsonResourceRepository(self.path, expression_parser)

    def json_grant_repository(
            self, expression_parser: ExpressionParser
    ) -> JsonGrantRepository:
        return JsonGrantRepository(self.path, expression_parser)

    def json_permission_repository(
            self, expression_parser: ExpressionParser
    ) -> JsonPermissionRepository:
        return JsonPermissionRepository(self.path, expression_parser)

    def json_import_service(
            self, hash_service: HashService) -> JsonImportService:
        return JsonImportService(hash_service)

    def json_catalog_service(
            self, expression_parser: ExpressionParser) -> JsonCatalogService:
        catalog_path = self.config['tenancy']['url']
        return JsonCatalogService(catalog_path, expression_parser)

    def json_provision_service(self) -> JsonProvisionService:
        data_directory = self.config['data']['dir']
        return JsonProvisionService(data_directory)
