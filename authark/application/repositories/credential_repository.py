from ..models import Credential
from .repository import Repository
from .memory_repository import MemoryRepository


class CredentialRepository(Repository[Credential]):
    """Credential Repository"""


class MemoryCredentialRepository(
        MemoryRepository[Credential], CredentialRepository):
    """Memory Credential Repository"""
