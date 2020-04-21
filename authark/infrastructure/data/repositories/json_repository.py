import os
from pathlib import Path
from json import load, dump
from uuid import uuid4
from typing import Dict, List, Any, Type, Callable, Generic, Union
from ....application.models import T
from ....application.repositories import Repository
from ....application.utilities import (
    QueryDomain, TenantProvider, QueryParser, EntityNotFoundError)


class JsonRepository(Repository, Generic[T]):
    def __init__(self,
                 data_path: str,
                 parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str,
                 item_class: Callable[..., T]) -> None:
        self.data_path = data_path
        self.parser = parser
        self.collection = collection
        self.item_class: Callable[..., T] = item_class
        self.tenant_provider = tenant_provider

    async def add(self, item: Union[T, List[T]]) -> List[T]:

        items = item if isinstance(item, list) else [item]
        data: Dict[str, Any] = {}
        with self._file_path.open() as f:
            data = load(f)

        for item in items:
            setattr(item, 'id', getattr(item, 'id') or str(uuid4()))
            data[self.collection].update({getattr(item, 'id'): vars(item)})

        with self._file_path.open('w') as f:
            dump(data, f, indent=2)

        return items

    async def search(self, domain: QueryDomain,
                     limit=10_000, offset=0) -> List[T]:
        
        with self._file_path.open() as f:
            data = load(f)
            items_dict = data.get(self.collection, {})

        items = []
        filter_function = self.parser.parse(domain)
        for item_dict in items_dict.values():
            item = self.item_class(**item_dict)

            if filter_function(item):
                items.append(item)

        if offset is not None:
            items = items[offset:]
        if limit is not None:
            items = items[:limit]

        return items

    async def remove(self, item: Union[T, List[T]]) -> bool:

        items = item if isinstance(item, list) else [item]
        data: Dict[str, Any] = {}
        with self._file_path.open() as f:
            data = load(f)

        for item in items:
            id = getattr(item, 'id')
            if id not in data[self.collection]:
                return False
            del data[self.collection][id]

        with self._file_path.open('w') as f:
            dump(data, f, indent=2)

        return True

    async def count(self, domain: QueryDomain = None) -> int:

        with self._file_path.open() as f:
            data = load(f)
            items_dict = data.get(self.collection, {})

        items = []
        filter_function = self.parser.parse(domain)
        for item_dict in items_dict.values():
            item = self.item_class(**item_dict)

            if filter_function(item):
                items.append(item)

        count = len(items)

        return count

    @property
    def _file_path(self) -> Path:
        zone = self.tenant_provider.tenant.zone
        path = Path(self.data_path) / zone / f"{ self.collection}.json"
        return path
