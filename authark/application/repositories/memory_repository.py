from abc import ABC, abstractmethod
from uuid import uuid4
from collections import defaultdict
from typing import List, Dict, TypeVar, Optional, Generic, Union
from ..utilities import (
    TenantProvider, ExpressionParser, QueryDomain, T, EntityNotFoundError)
from .repository import Repository


class MemoryRepository(Repository, Generic[T]):
    def __init__(self,  parser: ExpressionParser,
                 tenant_provider: TenantProvider) -> None:
        self.data: Dict[str, Dict[str, T]] = defaultdict(dict)
        self.parser = parser
        self.tenant_provider = tenant_provider

    def get(self, id: str) -> T:
        item = self.data[self._location].get(id)
        if not item:
            raise EntityNotFoundError(
                f"The entity with id {id} was not found.")
        return item

    def add(self, item: Union[T, List[T]]) -> List[T]:
        items = item if isinstance(item, list) else [item]
        for item in items:
            setattr(item, 'id', getattr(item, 'id') or str(uuid4()))
            self.data[self._location][getattr(item, 'id')] = item
        return items

    def update(self, item: Union[T, List[T]]) -> bool:
        items = item if isinstance(item, list) else [item]

        for item in items:
            id = getattr(item, 'id')
            if id not in self.data[self._location]:
                return False

        for item in items:
            id = getattr(item, 'id')
            self.data[self._location][id] = item

        return True

    def search(self, domain: QueryDomain, limit=1000, offset=0) -> List[T]:
        items = []
        filter_function = self.parser.parse(domain)
        for item in list(self.data[self._location].values()):
            if filter_function(item):
                items.append(item)

        if limit is not None:
            items = items[:limit]
        if offset is not None:
            items = items[offset:]

        return items

    def remove(self, item: Union[T, List[T]]) -> bool:
        items = item if isinstance(item, list) else [item]
        for item in items:
            id = getattr(item, 'id')
            if id not in self.data[self._location]:
                return False

        for item in items:
            id = getattr(item, 'id')
            del self.data[self._location][id]

        return True

    def load(self, data: Dict[str, Dict[str, T]]) -> None:
        self.data = data

    @property
    def _location(self) -> str:
        return self.tenant_provider.tenant.location
