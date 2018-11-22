from ..models import User
from .repository import Repository
from .memory_repository import MemoryRepository


class UserRepository(Repository[User]):
    """User Repository"""


class MemoryUserRepository(MemoryRepository[User], UserRepository):
    """Memory User Repository"""
