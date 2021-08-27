from modelark import JsonRepository
from ....application.domain.common import (
    QueryParser, AuthProvider)
from ....application.domain.models import (
    Credential, Dominion, Ranking, Role, User, Restriction, Policy)
from ....application.domain.repositories import (
    CredentialRepository, DominionRepository, RankingRepository,
    RoleRepository, UserRepository, RestrictionRepository, PolicyRepository)


class JsonCredentialRepository(JsonRepository, CredentialRepository):
    """Json Credential Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 auth_provider: AuthProvider,
                 collection: str = 'credentials') -> None:
        super().__init__(data_path, collection, Credential,
                         parser, auth_provider, auth_provider)


class JsonDominionRepository(JsonRepository, DominionRepository):
    """Json Dominion Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 auth_provider: AuthProvider,
                 collection: str = 'dominions') -> None:
        super().__init__(data_path, collection, Dominion,
                         parser, auth_provider, auth_provider)


class JsonRankingRepository(JsonRepository, RankingRepository):
    """Json Ranking Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 auth_provider: AuthProvider,
                 collection: str = 'rankings') -> None:
        super().__init__(data_path, collection, Ranking,
                         parser, auth_provider, auth_provider)


class JsonRoleRepository(JsonRepository, RoleRepository):
    """Json Role Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 auth_provider: AuthProvider,
                 collection: str = 'roles') -> None:
        super().__init__(data_path, collection, Role,
                         parser, auth_provider, auth_provider)


class JsonRestrictionRepository(JsonRepository, RestrictionRepository):
    """Json Restriction Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 auth_provider: AuthProvider,
                 collection: str = 'restrictions') -> None:
        super().__init__(data_path, collection, Restriction,
                         parser, auth_provider, auth_provider)


class JsonPolicyRepository(JsonRepository, PolicyRepository):
    """Json Policy Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 auth_provider: AuthProvider,
                 collection: str = 'policies') -> None:
        super().__init__(data_path, collection, Policy,
                         parser, auth_provider, auth_provider)


class JsonUserRepository(JsonRepository, UserRepository):
    """Json User Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 auth_provider: AuthProvider,
                 collection: str = 'users') -> None:
        super().__init__(data_path, collection, User,
                         parser, auth_provider, auth_provider)
