import os
import time
from pathlib import Path
from collections import defaultdict
from rapidjson import loads, load, dump
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

        data = defaultdict(lambda: {})  # type: Dict[str, Any]
        if self.file_path.exists():
            data.update(loads(self.file_path.read_text()))

        for item in items:
            item.id = item.id or str(uuid4())
            item.updated_at = int(time.time())
            if not data[self.collection].get(item.id):
                item.created_at = item.updated_at

            data[self.collection][item.id] = vars(item)

        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open('w') as f:
            dump(data, f, indent=2)

        return items

    async def search(self, domain: QueryDomain,
                     limit=10_000, offset=0) -> List[T]:

        if not self.file_path.exists():
            return []

        with self.file_path.open('r') as f:
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
        if not self.file_path.exists():
            return False

        with self.file_path.open('r') as f:
            data = load(f)

        deleted = False
        for item in items:
            deleted_item = data[self.collection].pop(item.id, None)
            deleted = bool(deleted_item) or deleted

        with self.file_path.open('w') as f:
            dump(data, f, indent=2)

        return deleted

    async def count(self, domain: QueryDomain = None) -> int:
        if not self.file_path.exists():
            return 0

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open('r') as f:
            data = load(f)

        count = 0
        domain = domain or []
        filter_function = self.parser.parse(domain)
        for item_dict in list(data[self.collection].values()):
            item = self.item_class(**item_dict)
            if filter_function(item):
                count += 1
        return count

    @property
    def file_path(self) -> Path:
        zone = self.tenant_provider.tenant.zone
        slug = self.tenant_provider.tenant.slug
        path = Path(self.data_path) / zone / slug / f"{self.collection}.json"
        return path
    # /opt/authark/data/c/knowark/dummies.json
