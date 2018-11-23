from abc import ABC
from authark.infrastructure.config.registry import Registry


class Context(ABC):
    def __init__(self):
        self.config = {}
        self.registry = {}
