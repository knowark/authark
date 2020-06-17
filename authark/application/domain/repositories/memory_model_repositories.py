from ..models import Credential, Dominion, Ranking, Role, User, Rule, Policy
from .repository import Repository
from .memory_repository import MemoryRepository


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


class RuleRepository(Repository[Rule]):
    model = Rule


class MemoryRuleRepository(
        MemoryRepository, RuleRepository):
    """Memory Rule Repository"""


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
