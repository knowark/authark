from ..models import Dominion
from .repository import Repository
from .memory_repository import MemoryRepository


class DominionRepository(Repository[Dominion]):
    """Dominion Repository"""


class MemoryDominionRepository(
        MemoryRepository[Dominion], DominionRepository):
    """Memory Dominion Repository"""
