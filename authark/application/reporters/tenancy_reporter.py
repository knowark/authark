from abc import ABC, abstractmethod
from authark.application.services import CatalogService
from ..utilities import QueryDomain
from .types import ResultDictList


class TenancyReporter(ABC):

    @abstractmethod
    def search_tenants(self, domain: QueryDomain) -> ResultDictList:
        """Search the system tenants"""


class StandardTenancyReporter(TenancyReporter):

    def __init__(self, catalog_service: CatalogService) -> None:
        self.catalog_service = catalog_service

    def search_tenants(self, domain: QueryDomain) -> ResultDictList:
        return [vars(tenant) for tenant in sorted(
            self.catalog_service.search_tenants(domain),
            key=lambda x: x.name)]
