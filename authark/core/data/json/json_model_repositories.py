from modelark import JsonRepository
from ....application.domain.common import TenantProvider, QueryParser
from ....application.domain.models import (
    Credential, Dominion, Ranking, Role, User, Restriction, Policy)
from ....application.domain.repositories import (
    CredentialRepository, DominionRepository, RankingRepository,
    RoleRepository, UserRepository, RestrictionRepository, PolicyRepository)


class JsonCredentialRepository(JsonRepository, CredentialRepository):
    """Json Credential Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str = 'credentials') -> None:
        super().__init__(data_path, parser, tenant_provider,
                         collection, Credential, )


class JsonDominionRepository(JsonRepository, DominionRepository):
    """Json Dominion Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str = 'dominions') -> None:
        super().__init__(data_path, collection, Dominion,
                         parser, tenant_provider)


class JsonRankingRepository(JsonRepository, RankingRepository):
    """Json Ranking Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str = 'rankings') -> None:
        super().__init__(data_path, collection, Ranking,
                         parser, tenant_provider)


class JsonRoleRepository(JsonRepository, RoleRepository):
    """Json Role Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str = 'roles') -> None:
        super().__init__(data_path, collection, Role,
                         parser, tenant_provider)


class JsonRestrictionRepository(JsonRepository, RestrictionRepository):
    """Json Restriction Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str = 'restrictions') -> None:
        super().__init__(data_path, collection, Restriction,
                         parser, tenant_provider)


class JsonPolicyRepository(JsonRepository, PolicyRepository):
    """Json Policy Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str = 'policies') -> None:
        super().__init__(data_path, collection, Policy,
                         parser, tenant_provider)


class JsonUserRepository(JsonRepository, UserRepository):
    """Json User Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str = 'users') -> None:
        super().__init__(data_path, collection, User,
                         parser, tenant_provider)
