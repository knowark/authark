import time
from uuid import uuid4
from collections import defaultdict
from typing import List, Dict, Generic, Union
from ..models import T
from ..common import QueryParser, QueryDomain, TenantProvider
from .repository import Repository


class MemoryRepository(Repository, Generic[T]):
    def __init__(self,  parser: QueryParser,
                 tenant_provider: TenantProvider) -> None:
        self.data: Dict[str, Dict[str, T]] = defaultdict(dict)
        self.parser: QueryParser = parser
        self.tenant_provider: TenantProvider = tenant_provider
        self.max_items = 10_000

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

    async def search(self, domain: QueryDomain,
                     limit=10000, offset=0) -> List[T]:
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

    async def remove(self, item: Union[T, List[T]]) -> bool:
        items = item if isinstance(item, list) else [item]
        deleted = False
        for item in items:
            if item.id not in self.data[self._location]:
                continue
            del self.data[self._location][item.id]
            deleted = True

        return deleted

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
