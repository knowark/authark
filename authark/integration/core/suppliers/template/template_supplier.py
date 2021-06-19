from typing import Dict, Any
from abc import ABC, abstractmethod


class TemplateSupplier(ABC):
    @abstractmethod
    def render(self, template: str, context: Dict[str, Any]):
        """Render method to be implemented."""


class MemoryTemplateSupplier(TemplateSupplier):
    def render(self, template: str, context: Dict[str, Any]):
        return f"{template}: {context}"
