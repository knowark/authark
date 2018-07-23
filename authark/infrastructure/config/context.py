from authark.infrastructure.config.config import Config
from authark.infrastructure.config.registry import Registry


class Context():
    def __init__(self, config: Config, registry: Registry):
        self.config = config
        self.registry = registry
