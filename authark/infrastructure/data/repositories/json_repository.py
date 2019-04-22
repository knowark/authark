import os
from pathlib import Path
from json import load, dump
from uuid import uuid4
from typing import Dict, List, Optional, Any, Type, TypeVar, Callable, Generic
from ....application.utilities import ExpressionParser, EntityNotFoundError
from ....application.services import TenantService
from ....application.repositories import (
    Repository, QueryDomain)


T = TypeVar('T')


class JsonRepository(Repository, Generic[T]):
    def __init__(self, data_path: str, parser: ExpressionParser,
                 tenant_service: TenantService,
                 collection_name: str, item_class: Type[T]) -> None:
        super().__init__(tenant_service)
        self.data_path = data_path
        self.parser = parser
        self.collection_name = collection_name
        self.item_class: Callable[..., T] = item_class

    def get(self, id: str) -> T:
        with self._file_path.open() as f:
            data = load(f)
            items = data.get(self.collection_name, {})
            item_dict = items.get(id)
            if not item_dict:
                raise EntityNotFoundError(
                    f"The entity with id {id} was not found.")
            return self.item_class(**item_dict)

    def add(self, item: T) -> T:
        data: Dict[str, Any] = {}
        with self._file_path.open() as f:
            data = load(f)
        setattr(item, 'id', getattr(item, 'id') or str(uuid4()))
        data[self.collection_name].update({getattr(item, 'id'): vars(item)})
        with self._file_path.open('w') as f:
            dump(data, f, indent=2)
        return item

    def update(self, item: T) -> bool:
        with self._file_path.open() as f:
            data = load(f)
            items_dict = data.get(self.collection_name)

        id = getattr(item, 'id')
        if id not in items_dict:
            return False

        items_dict[id] = vars(item)

        with self._file_path.open('w') as f:
            dump(data, f, indent=2)
        return True

    def search(self, domain: QueryDomain, limit=0, offset=0) -> List[T]:
        with self._file_path.open() as f:
            data = load(f)
            items_dict = data.get(self.collection_name, {})

        items = []
        limit = int(limit) if limit > 0 else 10000
        offset = int(offset) if offset > 0 else 0
        filter_function = self.parser.parse(domain)
        for item_dict in items_dict.values():
            item = self.item_class(**item_dict)

            if filter_function(item):
                items.append(item)

        items = items[:limit]
        items = items[offset:]

        return items

    def remove(self, item: T) -> bool:
        with self._file_path.open() as f:
            data = load(f)
            items_dict = data.get(self.collection_name)

        id = getattr(item, 'id')
        if id not in items_dict:
            return False

        del items_dict[id]

        with self._file_path.open('w') as f:
            dump(data, f, indent=2)
        return True

    @property
    def _file_path(self) -> Path:
        location = self.tenant_service.get_tenant().location
        return Path(self.data_path) / location / f"{location}.json"
