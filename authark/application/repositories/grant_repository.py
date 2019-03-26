from ..models import Grant
from .repository import Repository
from .memory_repository import MemoryRepository


class GrantRepository(Repository[Grant]):
    """Grant Repository"""


class MemoryGrantRepository(
        MemoryRepository[Grant], GrantRepository):
    """Memory Grant Repository"""
