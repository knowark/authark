from ..models import Policy
from .repository import Repository
from .memory_repository import MemoryRepository


class PolicyRepository(Repository[Policy]):
    """Policy Repository"""


class MemoryPolicyRepository(
        MemoryRepository[Policy], PolicyRepository):
    """Memory Policy Repository"""
