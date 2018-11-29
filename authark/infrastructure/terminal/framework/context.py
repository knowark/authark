from abc import ABC
from typing import Dict, Any


class Context(ABC):
    def __init__(self, config=None, registry=None):
        self.config = config or {}  # Dict[str, Any]
        self.registry = registry or {}  # Dict[str, Any]
