from abc import ABC, abstractmethod
from uuid import uuid4
from typing import List, Dict, Any
from .tenant import Tenant


class ProvisionService(ABC):
    """Tenant Provision service."""

    @abstractmethod
    def setup(self) -> bool:
        "Setup method to be implemented."

    @abstractmethod
    def create_tenant(self, tenant: Tenant) -> Tenant:
        "Create tenant method to be implemented."


class MemoryProvisionService(ProvisionService):

    def __init__(self) -> None:
        self.pool: Dict = None

    def setup(self) -> bool:
        self.pool = {}
        return True

    def create_tenant(self, tenant: Tenant) -> Tenant:
        tenant.id = tenant.id or str(uuid4())
        self.pool[tenant.id] = tenant
        return tenant
