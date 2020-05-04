from typing import List, Any
from abc import ABC, abstractmethod


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
