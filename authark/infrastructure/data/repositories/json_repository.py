import os
from pathlib import Path
from json import load, dump
from uuid import uuid4
from typing import Dict, List, Any, Type, Callable, Generic, Union
from ....application.services import TenantProvider
from ....application.models import T
from ....application.utilities import (
    QueryDomain, QueryParser, EntityNotFoundError)
from ....application.repositories import Repository


class JsonRepository(Repository, Generic[T]):
    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection: str, item_class: Callable[..., T]) -> None:
        self.data_path = data_path
        self.parser = parser
        self.collection = collection
        self.item_class: Callable[..., T] = item_class
        self.tenant_provider = tenant_provider

    def get(self, id: str) -> T:
        with self._file_path.open() as f:
            data = load(f)
            items = data.get(self.collection, {})
            item_dict = items.get(id)
            if not item_dict:
                raise EntityNotFoundError(
                    f"The entity with id {id} was not found.")
            return self.item_class(**item_dict)

    def add(self, item: Union[T, List[T]]) -> List[T]:
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

    def update(self, item: Union[T, List[T]]) -> bool:
        items = item if isinstance(item, list) else [item]
        data: Dict[str, Any] = {}
        with self._file_path.open() as f:
            data = load(f)

        for item in items:
            id = getattr(item, 'id')
            if id not in data[self.collection]:
                return False
            data[self.collection].update({id: vars(item)})

        with self._file_path.open('w') as f:
            dump(data, f, indent=2)

        return True

    def search(self, domain: QueryDomain, limit=1000, offset=0) -> List[T]:
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

    def remove(self, item: Union[T, List[T]]) -> bool:
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

    @property
    def _file_path(self) -> Path:
        location = self.tenant_provider.tenant.location
        path = Path(self.data_path) / location / f"{ self.collection}.json"
        return path
