from abc import ABC, abstractmethod
from typing import List, Generic, Union
from ..common import QueryDomain
from ..models import T


class Repository(ABC, Generic[T]):

    @abstractmethod
    async def add(self, item: Union[T, List[T]]) -> List[T]:
        "Add method to be implemented."

    @abstractmethod
    async def search(self, domain: QueryDomain,
                     limit: int = None, offset: int = None) -> List[T]:
        "Search items matching a query domain"

    @abstractmethod
    async def remove(self, item: Union[T, List[T]]) -> bool:
        "Remove method to be implemented."

    @abstractmethod
    async def count(self, domain: QueryDomain = None) -> int:
        "Count items matching a query domain"
