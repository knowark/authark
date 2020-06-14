from abc import ABC
from typing import Dict, Any


class Context(ABC):
    def __init__(self, config=None, resolver=None):
        self.config = config or {}  # Dict[str, Any]
        self.resolver = resolver

    def resolve(self, dependency: str):
        return self.resolver[dependency]
