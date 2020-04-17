# from ..models import (
#     Credential, Dominion, Ranking, Role, User)
from .repository import Repository
from .memory_repository import MemoryRepository


class CredentialRepository(Repository):
    """Credential Repository"""


class MemoryCredentialRepository(
        MemoryRepository, CredentialRepository):
    """Memory Credential Repository"""


class DominionRepository(Repository):
    """Dominion Repository"""


class MemoryDominionRepository(
        MemoryRepository, DominionRepository):
    """Memory Dominion Repository"""


class RankingRepository(Repository):
    """Ranking Repository"""


class MemoryRankingRepository(
        MemoryRepository, RankingRepository):
    """Memory Ranking Repository"""


class RoleRepository(Repository):
    """Role Repository"""


class MemoryRoleRepository(
        MemoryRepository, RoleRepository):
    """Memory Role Repository"""


class UserRepository(Repository):
    """User Repository"""


class MemoryUserRepository(
        MemoryRepository, UserRepository):
    """Memory User Repository"""


# forma anterior

# class CredentialRepository(Repository[Credential]):
#     """Credential Repository"""


# class MemoryCredentialRepository(
#         MemoryRepository[Credential], CredentialRepository):
#     """Memory Credential Repository"""


# class DominionRepository(Repository[Dominion]):
#     """Dominion Repository"""


# class MemoryDominionRepository(
#         MemoryRepository[Dominion], DominionRepository):
#     """Memory Dominion Repository"""

#     class RankingRepository(Repository[Ranking]):
#     """Ranking Repository"""


# class MemoryRankingRepository(
#         MemoryRepository[Ranking], RankingRepository):
#     """Memory Ranking Repository"""

#     class RoleRepository(Repository[Role]):
#     """Role Repository"""


# class MemoryRoleRepository(
#         MemoryRepository[Role], RoleRepository):
#     """Memory Role Repository"""


# class UserRepository(Repository[User]):
#     """User Repository"""


# class MemoryUserRepository(MemoryRepository[User], UserRepository):
#     """Memory User Repository"""
