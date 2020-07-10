import jwt
from ..core.common import Config
from .crypto_factory import CryptoFactory
from ..application.domain.common import (
    QueryParser, TenantProvider, StandardTenantProvider, Tenant,
    AuthProvider, StandardAuthProvider, User as CUser)
from ..application.domain.models import (
    User, Credential, Ranking, Role, Dominion, Restriction, Policy)
from ..application.domain.repositories import (
    MemoryUserRepository, MemoryCredentialRepository,
    RankingRepository, MemoryRankingRepository,
    RoleRepository, MemoryRoleRepository,
    RestrictionRepository, MemoryRestrictionRepository,
    PolicyRepository, MemoryPolicyRepository,
    DominionRepository, MemoryDominionRepository)
from ..application.domain.services import (
    AccessService, AccessTokenService)
from ..core import (
    MemoryTenantSupplier, PyJWTAccessTokenService)


class CheckFactory(CryptoFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def check_tenant_provider(self) -> StandardTenantProvider:
        tenant_provider = StandardTenantProvider()
        tenant_provider.setup(Tenant(id='001', name="Default"))
        return tenant_provider

    def check_auth_provider(self) -> StandardAuthProvider:
        auth_provider = StandardAuthProvider()
        auth_provider.setup(CUser(id='001', name='johndoe'))
        return auth_provider

    def check_tenant_supplier(self) -> MemoryTenantSupplier:
        tenant_supplier = MemoryTenantSupplier()
        tenant_supplier.create_tenant({
            'id': '001',
            'name': 'Default',
            'zone': 'default'
        })
        return tenant_supplier

    def memory_user_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
            # auth_provider: AuthProvider
    ) -> MemoryUserRepository:
        user_repository = super().memory_user_repository(
            query_parser, tenant_provider)
        user_repository.load({'default': {
            '1': User(
                id="1",
                username="eecheverry",
                email="eecheverry@nubark.com"),
            '2': User(
                id="2",
                username="mvivas",
                email="mvivas@gmail.com")
        }})
        return user_repository

    def memory_credential_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
            # auth_provider: AuthProvider
    ) -> MemoryCredentialRepository:
        credential_repository = super().memory_credential_repository(
            query_parser, tenant_provider)
        refresh_token = jwt.encode(
            {'user': "pepe"}, 'REFRESHSECRET').decode('utf-8')
        credential_repository.load({'default': {
            "1": Credential(id='1', user_id='1', value="HASHED: ABC1234"),
            "2": Credential(id='2', user_id='2', value="HASHED: XYZ098"),
            "3": Credential(id='3', user_id='1', value=refresh_token,
                            type='refresh_token')
        }})
        return credential_repository

    def memory_role_repository(
        self, query_parser: QueryParser,
        tenant_provider: TenantProvider
        # auth_provider: AuthProvider
    ) -> MemoryRoleRepository:
        role_repository = super().memory_role_repository(
            query_parser, tenant_provider)
        role_repository.load({'default': {
            "1": Role(id='1', name='admin', dominion_id='1',
                      description="Service's Administrator")
        }})
        return role_repository

    def memory_ranking_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
            # auth_provider: AuthProvider
    ) -> MemoryRankingRepository:
        ranking_repository = super().memory_ranking_repository(
            query_parser, tenant_provider)
        ranking_repository.load({'default': {
            "1": Ranking(id='1', user_id='1', role_id='1',
                         description="Service's Administrator")
        }})
        return ranking_repository

    def memory_restriction_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
    ) -> MemoryRestrictionRepository:
        restriction_repository = super().memory_restriction_repository(
            query_parser, tenant_provider)
        restriction_repository.load({'default': {
            "1": Restriction(id='1', sequence='1',
                             name="name group", policy_id='1',
                             target="target name", domain="domain")
        }})
        return restriction_repository

    def memory_policy_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
    ) -> MemoryPolicyRepository:
        policy_repository = super().memory_policy_repository(
            query_parser, tenant_provider)
        policy_repository.load({'default': {
            "1": Policy(id='1', resource='resource', privilege='privilege',
                        role_id="1")
        }})
        return policy_repository

    def memory_dominion_repository(
            self, query_parser: QueryParser,
            tenant_provider: TenantProvider
            # auth_provider: AuthProvider
    ) -> MemoryDominionRepository:
        dominion_repository = super().memory_dominion_repository(
            query_parser, tenant_provider)
        dominion_repository.load({'default': {
            "1": Dominion(id='1', name='Data Server',
                          url="https://dataserver.nubark.com")
        }})
        return dominion_repository

    def pyjwt_access_token_service(self) -> PyJWTAccessTokenService:
        access_token_service = PyJWTAccessTokenService(
            'TESTSECRET', 'HS256', 3600)
        return access_token_service

    def access_service(
            self, ranking_repository: RankingRepository,
            role_repository: RoleRepository,
            dominion_repository: DominionRepository,
            token_service: AccessTokenService,
            tenant_provider: TenantProvider) -> AccessService:
        return AccessService(
            ranking_repository, role_repository,
            dominion_repository, token_service, tenant_provider)
