from ..models import Role
from .repository import Repository
from .memory_repository import MemoryRepository


class RoleRepository(Repository[Role]):
    """Role Repository"""


class MemoryRoleRepository(
        MemoryRepository[Role], RoleRepository):
    """Memory Role Repository"""
