from ...application.domain.common import QueryParser, TenantProvider
from ...application.domain.services import HashService
from ..core.data import (
    JsonCredentialRepository, JsonDominionRepository, JsonRoleRepository,
    JsonUserRepository, JsonRankingRepository, JsonImportService)
from ..core.common import Config
from ..core.suppliers.tenancy import TenantSupplier, JsonTenantSupplier
from .crypto_factory import CryptoFactory


class JsonFactory(CryptoFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.data_path = self.config['zones']['default']['data']

    # Repositories

    def json_user_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
    ) -> JsonUserRepository:
        return JsonUserRepository(self.data_path, query_parser,
                                  tenant_provider)

    def json_credential_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
    ) -> JsonCredentialRepository:
        return JsonCredentialRepository(self.data_path, query_parser,
                                        tenant_provider)

    def json_dominion_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
    ) -> JsonDominionRepository:
        return JsonDominionRepository(self.data_path, query_parser,
                                      tenant_provider)

    def json_role_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
    ) -> JsonRoleRepository:
        return JsonRoleRepository(self.data_path, query_parser,
                                  tenant_provider)

    def json_ranking_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
    ) -> JsonRankingRepository:
        return JsonRankingRepository(self.data_path, query_parser,
                                     tenant_provider)

    def json_import_service(
            self, hash_service: HashService) -> JsonImportService:
        return JsonImportService(hash_service)

    def json_tenant_supplier(self) -> TenantSupplier:
        catalog_path = self.config['tenancy']['json']
        zones = {key: value['data'] for key, value in
                 self.config['zones'].items()}
        return JsonTenantSupplier(catalog_path, zones)
