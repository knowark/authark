import time
from uuid import uuid4
from collections import defaultdict
from typing import List, Dict, TypeVar, Optional, Type, Generic, Union, Any
from ..models import T
from ..utilities import (
    QueryParser, QueryDomain, TenantProvider, EntityNotFoundError)
from .repository import Repository


class MemoryRepository(Repository, Generic[T]):
    def __init__(self,  parser: QueryParser,
                 tenant_provider: TenantProvider) -> None:
        self.data: Dict[str, Dict[str, T]] = defaultdict(dict)
        self.parser: QueryParser = parser
        self.tenant_provider = tenant_provider
        self.max_items = 10_000

    # def get(self, id: str) -> T:
    #     item = self.data[self._location].get(id)
    #     if not item:
    #         raise EntityNotFoundError(
    #             f"The entity with id {id} was not found.")
    #     return item

    async def add(self, item: Union[T, List[T]]) -> List[T]:
        items = item if isinstance(item, list) else [item]
        for item in items:
            item.id = item.id or str(uuid4())
            item.updated_at = int(time.time())
            existing_item = self.data[self._location].get(item.id)
            if existing_item:
                item.created_at = existing_item.created_at
            else:
                item.created_at = item.updated_at

            self.data[self._location][item.id] = item
        return items

    # async def add(self, item: Union[T, List[T]]) -> List[T]:
    #     items = item if isinstance(item, list) else [item]
    #     for item in items:
    #         setattr(item, 'id', getattr(item, 'id') or str(uuid4()))
    #         self.data[self._location][getattr(item, 'id')] = item
    #     return items

    # def update(self, item: Union[T, List[T]]) -> bool:
    #     items = item if isinstance(item, list) else [item]

    #     for item in items:
    #         id = getattr(item, 'id')
    #         if id not in self.data[self._location]:
    #             return False

    #     for item in items:
    #         id = getattr(item, 'id')
    #         self.data[self._location][id] = item

    #     return True

    async def search(self, domain: QueryDomain,
                     limit=10_000, offset=0) -> List[T]:
        items = []
        filter_function = self.parser.parse(domain)
        for item in list(self.data[self._location].values()):
            if filter_function(item):
                items.append(item)

        if offset is not None:
            items = items[offset:]

        if limit is not None:
            items = items[:min(limit, self.max_items)]

        return items

    # def search(self, domain: QueryDomain, limit=1000, offset=0) -> List[T]:
    #     items = []
    #     filter_function = self.parser.parse(domain)
    #     for item in list(self.data[self._location].values()):
    #         if filter_function(item):
    #             items.append(item)

    #     if limit is not None:
    #         items = items[:limit]
    #     if offset is not None:
    #         items = items[offset:]

    #     return items

    async def remove(self, item: Union[T, List[T]]) -> bool:
        items = item if isinstance(item, list) else [item]
        deleted = False
        for item in items:
            deleted_item = self.data[self._location].pop(item.id, None)
            deleted = bool(deleted_item) or deleted

        return deleted

    # def remove(self, item: Union[T, List[T]]) -> bool:
    #     items = item if isinstance(item, list) else [item]
    #     for item in items:
    #         id = getattr(item, 'id')
    #         if id not in self.data[self._location]:
    #             return False

    #     for item in items:
    #         id = getattr(item, 'id')
    #         del self.data[self._location][id]

    #     return True

    async def count(self, domain: QueryDomain = None) -> int:
        count = 0
        domain = domain or []
        filter_function = self.parser.parse(domain)
        for item in list(self.data[self._location].values()):
            if filter_function(item):
                count += 1
        return count

    def load(self, data: Dict[str, Dict[str, T]]) -> None:
        self.data = data

    @property
    def _location(self) -> str:
        return self.tenant_provider.tenant.zone or 'default'

    # @property
    # def _location(self) -> str:
    #     return self.tenant_provider.tenant.location
