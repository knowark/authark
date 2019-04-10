from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .errors import AuthenticationError, AuthorizationError
from .token import Token
from .user import User


class TenantService(ABC):
    """Tenant service."""


class StandardTenantService(TenantService):

    def __init__(self, catalog_service: CatalogService) -> None:
        self.catalog_service = catalog_service
