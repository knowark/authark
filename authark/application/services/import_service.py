import json
from typing import Dict, List, Any
from abc import ABC, abstractmethod
from ..models import User


class ImportService(ABC):
    @abstractmethod
    def import_users(self, filepath: str, source: str,
                     password_field: str) -> List[Any]:
        "Import users method to be implemented."


class MemoryImportService(ImportService):
    def __init__(self):
        self.users = []

    def import_users(self, filepath: str, source: str,
                     password_field: str) -> List[Any]:
        return self.users
