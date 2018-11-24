from ..models import Ranking
from .repository import Repository
from .memory_repository import MemoryRepository


class RankingRepository(Repository[Ranking]):
    """Ranking Repository"""


class MemoryRankingRepository(
        MemoryRepository[Ranking], RankingRepository):
    """Memory Ranking Repository"""
