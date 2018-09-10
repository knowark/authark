from authark.application.models.credential import Credential
from authark.application.repositories.repository import Repository
from authark.application.repositories.memory_repository import MemoryRepository


class CredentialRepository(Repository[Credential]):
    """Credential Repository"""


class MemoryCredentialRepository(
        MemoryRepository[Credential], CredentialRepository):
    """Memory Credential Repository"""
