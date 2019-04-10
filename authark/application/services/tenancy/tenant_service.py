from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .catalog_service import CatalogService


class TenantService(ABC):
    """Tenant service."""


class StandardTenantService(TenantService):

    def __init__(self, catalog_service: CatalogService) -> None:
        self.catalog_service = catalog_service
