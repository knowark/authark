import jwt
from ..core.common import Config
from .crypto_factory import CryptoFactory
from ...application.domain.common import (
    QueryParser, AuthProvider, StandardAuthProvider, User as CUser)
from ...application.domain.models import (
    User, Credential, Ranking, Role, Dominion, Restriction, Policy)
from ...application.domain.services.repositories import (
    UserRepository, MemoryUserRepository,
    CredentialRepository, MemoryCredentialRepository,
    RankingRepository, MemoryRankingRepository,
    RoleRepository, MemoryRoleRepository,
    RestrictionRepository, MemoryRestrictionRepository,
    PolicyRepository, MemoryPolicyRepository,
    DominionRepository, MemoryDominionRepository)
from ...application.domain.services import (
    HashService, MemoryHashService,
    AccessService, AccessTokenService)
from ...application.general.suppliers import (
    TenantSupplier, MemoryTenantSupplier)
from ..core import PyJWTAccessTokenService


class CheckFactory(CryptoFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def auth_provider(self) -> AuthProvider:
        auth_provider = StandardAuthProvider()
        auth_provider.setup(CUser(
            id='001', tid='001', name='johndoe',
            tenant='default', organization='Default'))
        return auth_provider

    def tenant_supplier(self) -> TenantSupplier:
        tenant_supplier = MemoryTenantSupplier()
        tenant_supplier.create_tenant({
            'id': '001',
            'name': 'Default',
            'email': 'gabeche@gmail.com'
        })
        return tenant_supplier

    def hash_service(self) -> HashService:
        return MemoryHashService()

    def user_repository(
            self, query_parser: QueryParser,
            auth_provider: AuthProvider
    ) -> UserRepository:
        user_repository = super().user_repository(
            query_parser, auth_provider)
        user_repository.load({'default': {
            '1': User(
                id="1",
                username="eecheverry",
                email="eecheverry@knowark.com"),
            '2': User(
                id="2",
                username="mvivas",
                email="mvivas@gmail.com")
        }})
        return user_repository

    def credential_repository(
            self, query_parser: QueryParser,
            auth_provider: AuthProvider
    ) -> CredentialRepository:
        credential_repository = super().credential_repository(
            query_parser, auth_provider)
        refresh_token = jwt.encode(
            {'user': "pepe"}, 'REFRESHSECRET')
        credential_repository.load({'default': {
            "1": Credential(id='1', user_id='1', value="HASHED: ABC1234"),
            "2": Credential(id='2', user_id='2', value="HASHED: XYZ098"),
            "3": Credential(id='3', user_id='1', value=refresh_token,
                            type='refresh_token')
        }})
        return credential_repository

    def role_repository(
        self, query_parser: QueryParser,
        auth_provider: AuthProvider
    ) -> RoleRepository:
        role_repository = super().role_repository(
            query_parser, auth_provider)
        role_repository.load({'default': {
            "1": Role(id='1', name='admin', dominion_id='1',
                      description="Service's Administrator")
        }})
        return role_repository

    def ranking_repository(
            self, query_parser: QueryParser,
            auth_provider: AuthProvider
    ) -> RankingRepository:
        ranking_repository = super().ranking_repository(
            query_parser, auth_provider)
        ranking_repository.load({'default': {
            "1": Ranking(id='1', user_id='1', role_id='1',
                         description="Service's Administrator")
        }})
        return ranking_repository

    def restriction_repository(
            self, query_parser: QueryParser,
            auth_provider: AuthProvider
    ) -> RestrictionRepository:
        restriction_repository = super().restriction_repository(
            query_parser, auth_provider)
        restriction_repository.load({'default': {
            "1": Restriction(id='1', sequence='1',
                             name="name group", policy_id='1',
                             target="target name", domain="domain")
        }})
        return restriction_repository

    def policy_repository(
            self, query_parser: QueryParser,
            auth_provider: AuthProvider
    ) -> PolicyRepository:
        policy_repository = super().policy_repository(
            query_parser, auth_provider)
        policy_repository.load({'default': {
            "1": Policy(id='1', resource='resource', privilege='privilege',
                        role_id="1")
        }})
        return policy_repository

    def dominion_repository(
            self, query_parser: QueryParser,
            auth_provider: AuthProvider
    ) -> DominionRepository:
        dominion_repository = super().dominion_repository(
            query_parser, auth_provider)
        dominion_repository.load({'default': {
            "1": Dominion(id='1', name='default')
        }})
        return dominion_repository

    def access_token_service(self) -> AccessTokenService:
        access_token_service = PyJWTAccessTokenService(
            'TESTSECRET', 'HS256', 3600)
        return access_token_service

    def access_service(
            self, ranking_repository: RankingRepository,
            role_repository: RoleRepository,
            dominion_repository: DominionRepository,
            token_service: AccessTokenService) -> AccessService:
        return AccessService(
            ranking_repository, role_repository,
            dominion_repository, token_service)
