from abc import ABC, abstractmethod
from typing import List, TypeVar, Optional, Generic
from .types import QueryDomain, T


class Repository(ABC, Generic[T]):

    @abstractmethod
    def get(self, id: str) -> Optional[T]:
        "Get method to be implemented."

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
