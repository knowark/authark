from abc import ABC, abstractmethod
from typing import List, Generic, Union
from ..utilities import T, QueryDomain


class Repository(ABC, Generic[T]):

    @abstractmethod
    def get(self, id: str) -> T:
        "Get method to be implemented. Raises if missing."

    @abstractmethod
    def add(self, item: Union[T, List[T]]) -> List[T]:
        "Add method to be implemented."

    @abstractmethod
    def update(self, item: Union[T, List[T]]) -> bool:
        "Update method to be implemented."

    @abstractmethod
    def search(self, domain: QueryDomain, limit=0, offset=0) -> List[T]:
        "Search users matching a query domain"

    @abstractmethod
    def remove(self, item: Union[T, List[T]]) -> bool:
        "Remove method to be implemented."
