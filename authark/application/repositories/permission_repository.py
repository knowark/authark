from ..models import Permission
from .repository import Repository
from .memory_repository import MemoryRepository


class PermissionRepository(Repository[Permission]):
    """Permission Repository"""


class MemoryPermissionRepository(
        MemoryRepository[Permission], PermissionRepository):
    """Memory Permission Repository"""
