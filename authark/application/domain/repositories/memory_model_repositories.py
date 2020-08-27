from modelark import Repository, MemoryRepository
from ..models import (
    Credential, Dominion, Ranking, Role, User, Restriction, Policy)


class CredentialRepository(Repository[Credential]):
    model = Credential


class MemoryCredentialRepository(
        MemoryRepository, CredentialRepository):
    """Memory Credential Repository"""


class DominionRepository(Repository[Dominion]):
    model = Dominion


class MemoryDominionRepository(
        MemoryRepository, DominionRepository):
    """Memory Dominion Repository"""


class RankingRepository(Repository[Ranking]):
    model = Ranking


class MemoryRankingRepository(
        MemoryRepository, RankingRepository):
    """Memory Ranking Repository"""


class RoleRepository(Repository[Role]):
    model = Role


class MemoryRoleRepository(
        MemoryRepository, RoleRepository):
    """Memory Role Repository"""


class RestrictionRepository(Repository[Restriction]):
    model = Restriction


class MemoryRestrictionRepository(
        MemoryRepository, RestrictionRepository):
    """Memory Restriction Repository"""


class PolicyRepository(Repository[Policy]):
    model = Policy


class MemoryPolicyRepository(
        MemoryRepository, PolicyRepository):
    """Memory Policy Repository"""


class UserRepository(Repository[User]):
    model = User


class MemoryUserRepository(
        MemoryRepository, UserRepository):
    """Memory User Repository"""
