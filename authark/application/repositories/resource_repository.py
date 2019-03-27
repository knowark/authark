from ..models import Resource
from .repository import Repository
from .memory_repository import MemoryRepository


class ResourceRepository(Repository[Resource]):
    """Resource Repository"""


class MemoryResourceRepository(
        MemoryRepository[Resource], ResourceRepository):
    """Memory Resource Repository"""
