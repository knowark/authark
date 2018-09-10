from authark.application.models.user import User
from authark.application.repositories.repository import Repository
from authark.application.repositories.memory_repository import MemoryRepository


class UserRepository(Repository[User]):
    """User Repository"""


class MemoryUserRepository(MemoryRepository[User], UserRepository):
    """Memory User Repository"""
