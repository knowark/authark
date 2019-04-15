from abc import ABC, abstractmethod
from typing import List, TypeVar, Optional, Generic
from ..services import TenantService
from ..utilities import QueryDomain, T


class Repository(ABC, Generic[T]):

    @abstractmethod
    def __init__(self, tenant_service: TenantService) -> None:
        "__init__ method to be implemented."
        self.tenant_service = tenant_service

    @abstractmethod
    def get(self, id: str) -> T:
        "Get method to be implemented. Raises if missing."

    @abstractmethod
    def add(self, item: T) -> T:
        "Add method to be implemented."

    @abstractmethod
    def update(self, item: T) -> bool:
        "Update method to be implemented."

    @abstractmethod
    def search(self, domain: QueryDomain, limit=0, offset=0) -> List[T]:
        "Search users matching a query domain"

    @abstractmethod
    def remove(self, item: T) -> bool:
        "Remove method to be implemented."
