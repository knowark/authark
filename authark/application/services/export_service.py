import json
from typing import List
from abc import ABC, abstractmethod
from .tenancy import Tenant


class ExportService(ABC):
    @abstractmethod
    def export_tenants(self, tenants: List[Tenant]) -> None:
        "Export tenants method to be implemented."


class MemoryExportService(ExportService):
    def __init__(self):
        self.tenants = []

    def export_tenants(self, tenants: List[Tenant]) -> None:
        self.tenants = tenants
