from ....application.domain.common import TenantProvider, QueryParser
from ....application.domain.models import (
    Credential, Dominion, Ranking, Role, User, Rule, Policy)
from ....application.domain.repositories import (
    CredentialRepository, DominionRepository, RankingRepository,
    RoleRepository, UserRepository, RuleRepository, PolicyRepository)
from .json_repository import JsonRepository


class JsonCredentialRepository(JsonRepository, CredentialRepository):
    """Json Credential Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str = 'credentials') -> None:
        super().__init__(data_path, parser, tenant_provider,
                         collection, Credential)


class JsonDominionRepository(JsonRepository, DominionRepository):
    """Json Dominion Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str = 'dominions') -> None:
        super().__init__(data_path, parser, tenant_provider,
                         collection, Dominion)


class JsonRankingRepository(JsonRepository, RankingRepository):
    """Json Ranking Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str = 'rankings') -> None:
        super().__init__(data_path, parser, tenant_provider,
                         collection, Ranking)


class JsonRoleRepository(JsonRepository, RoleRepository):
    """Json Role Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str = 'roles') -> None:
        super().__init__(data_path, parser, tenant_provider,
                         collection, Role)


class JsonRuleRepository(JsonRepository, RuleRepository):
    """Json Rule Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str = 'rules') -> None:
        super().__init__(data_path, parser, tenant_provider,
                         collection, Rule)


class JsonPolicyRepository(JsonRepository, PolicyRepository):
    """Json Policy Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str = 'policies') -> None:
        super().__init__(data_path, parser, tenant_provider,
                         collection, Policy)


class JsonUserRepository(JsonRepository, UserRepository):
    """Json User Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str = 'users') -> None:
        super().__init__(data_path, parser, tenant_provider,
                         collection, User)
