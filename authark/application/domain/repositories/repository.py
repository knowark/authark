from abc import ABC, abstractmethod
from typing import Type, List, Generic, Union, overload
from ..common import QueryDomain
from ..models import T, R, L


class Repository(ABC, Generic[T]):
    @property
    def model(self) -> Type[T]:
        raise NotImplementedError('Provide the repository model')

    @abstractmethod
    async def add(self, item: Union[T, List[T]]) -> List[T]:
        "Add method to be implemented."

    @abstractmethod
    async def remove(self, item: Union[T, List[T]]) -> bool:
        "Remove method to be implemented."

    @abstractmethod
    async def count(self, domain: QueryDomain = None) -> int:
        "Count items matching a query domain"

    @overload
    async def search(self, domain: QueryDomain,
                     limit: int = None, offset: int = None) -> List[T]:
        """Standard search method"""

    @overload
    async def search(self, domain: QueryDomain,
                     limit: int = None, offset: int = None,
                     *,
                     join: 'Repository[R]' = None,
                     link: 'Repository[L]' = None,
                     target: str = None, source: str = None) -> List[R]:
        """Joining search method"""

    @abstractmethod
    async def search(
            self, domain: QueryDomain,
            limit: int = None,
            offset: int = None,
            *,
            join: 'Repository[R]' = None,
            link: 'Repository[L]' = None,
            target: str = None, source: str = None) -> Union[List[T], List[R]]:
        "Search items matching a query domain"
