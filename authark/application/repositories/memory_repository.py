from abc import ABC, abstractmethod
from uuid import uuid4
from typing import List, Dict, TypeVar, Optional, Generic
from ..services import TenantService
from ..utilities import ExpressionParser, QueryDomain, T
from .repository import Repository
from .errors import EntityNotFoundError


class MemoryRepository(Repository, Generic[T]):
    def __init__(self,  parser: ExpressionParser,
                 tenant_service: TenantService,
                 tenants: List[str]) -> None:
        super().__init__(tenant_service)
        if not tenants:
            raise ValueError("At least one tenant must be provided.")

        self.data: Dict[str, Dict[str, T]] = {
            tenant: {} for tenant in tenants
        }

        self.parser = parser

    def get(self, id: str) -> T:
        slug = self.tenant_service.get_tenant().slug
        item = self.data[slug].get(id)
        if not item:
            raise EntityNotFoundError(
                f"The entity with id {id} was not found.")
        return item

    def add(self, item: T) -> T:
        slug = self.tenant_service.get_tenant().slug
        setattr(item, 'id', getattr(item, 'id') or str(uuid4()))
        self.data[slug][getattr(item, 'id')] = item
        # self.items[getattr(item, 'id')] = item
        return item

    def update(self, item: T) -> bool:
        slug = self.tenant_service.get_tenant().slug
        id = getattr(item, 'id')
        if id not in self.data[slug]:
            return False
        self.data[slug][id] = item
        return True

    def search(self, domain: QueryDomain, limit=0, offset=0) -> List[T]:
        slug = self.tenant_service.get_tenant().slug
        items = []
        limit = int(limit) if limit > 0 else 10000
        offset = int(offset) if offset > 0 else 0
        filter_function = self.parser.parse(domain)
        for item in list(self.data[slug].values()):
            if filter_function(item):
                items.append(item)

        items = items[:limit]
        items = items[offset:]

        return items

    def remove(self, item: T) -> bool:
        slug = self.tenant_service.get_tenant().slug
        id = getattr(item, 'id')
        if id not in self.data[slug]:
            return False
        del self.data[slug][id]
        return True

    def load(self, data: Dict[str, Dict[str, T]]) -> None:
        self.data = data
