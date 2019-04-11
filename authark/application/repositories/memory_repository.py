from abc import ABC, abstractmethod
from uuid import uuid4
from typing import List, Dict, TypeVar, Optional, Generic
from .repository import Repository
from .expression_parser import ExpressionParser
from .types import QueryDomain, T
from .errors import EntityNotFoundError


class MemoryRepository(Repository, Generic[T]):
    def __init__(self,  parser: ExpressionParser) -> None:
        self.items = {}  # type: Dict[str, T]
        self.parser = parser

    def get(self, id: str) -> T:
        item = self.items.get(id)
        if not item:
            raise EntityNotFoundError(
                f"The entity with id {id} was not found.")
        return item

    def add(self, item: T) -> T:
        setattr(item, 'id', getattr(item, 'id') or str(uuid4()))
        self.items[getattr(item, 'id')] = item
        return item

    def update(self, item: T) -> bool:
        id = getattr(item, 'id')
        if id not in self.items:
            return False
        self.items[id] = item
        return True

    def search(self, domain: QueryDomain, limit=0, offset=0) -> List[T]:
        items = []
        limit = int(limit) if limit > 0 else 10000
        offset = int(offset) if offset > 0 else 0
        filter_function = self.parser.parse(domain)
        for item in list(self.items.values()):
            if filter_function(item):
                items.append(item)

        items = items[:limit]
        items = items[offset:]

        return items

    def remove(self, item: T) -> bool:
        id = getattr(item, 'id')
        if id not in self.items:
            return False
        del self.items[id]
        return True

    def load(self, items: Dict[str, T]) -> None:
        self.items = items
