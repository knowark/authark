from ..application.domain.common import (
    QueryParser, TenantProvider, AuthProvider)
from ..application.domain.repositories import (
    UserRepository, CredentialRepository,
    DominionRepository, RoleRepository,
    RankingRepository, RestrictionRepository,
    PolicyRepository)
from ..application.domain.services import HashService, ImportService
from ..core.data import (
    JsonCredentialRepository, JsonDominionRepository, JsonRoleRepository,
    JsonUserRepository, JsonRankingRepository, JsonImportService,
    JsonRestrictionRepository, JsonPolicyRepository)
from ..core.common import Config
from ..core.suppliers import (
    TenantSupplier, JsonTenantSupplier, SetupSupplier, JsonSetupSupplier)
from .crypto_factory import CryptoFactory


class JsonFactory(CryptoFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.data_path = self.config['zones']['default']['data']

    # Repositories

    def user_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> UserRepository:
        return JsonUserRepository(self.data_path, query_parser,
                                  tenant_provider, auth_provider)

    def credential_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> CredentialRepository:
        return JsonCredentialRepository(self.data_path, query_parser,
                                        tenant_provider, auth_provider)

    def dominion_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> DominionRepository:
        return JsonDominionRepository(self.data_path, query_parser,
                                      tenant_provider, auth_provider)

    def role_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> RoleRepository:
        return JsonRoleRepository(self.data_path, query_parser,
                                  tenant_provider, auth_provider)

    def restriction_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> RestrictionRepository:
        return JsonRestrictionRepository(self.data_path, query_parser,
                                         tenant_provider, auth_provider)

    def policy_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> PolicyRepository:
        return JsonPolicyRepository(self.data_path, query_parser,
                                    tenant_provider, auth_provider)

    def ranking_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider,
            auth_provider: AuthProvider
    ) -> RankingRepository:
        return JsonRankingRepository(self.data_path, query_parser,
                                     tenant_provider, auth_provider)

    def import_service(self, hash_service: HashService) -> ImportService:
        return JsonImportService(hash_service)

    def tenant_supplier(self) -> TenantSupplier:
        catalog_path = self.config['tenancy']['json']
        zones = {key: value['data'] for key, value in
                 self.config['zones'].items()}
        return JsonTenantSupplier(catalog_path, zones)

    def setup_supplier(self) -> SetupSupplier:
        zones = {key: value['data'] for key, value in
                 self.config['zones'].items()}
        return JsonSetupSupplier(zones)
