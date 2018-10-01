from pytest import fixture
from authark.infrastructure.config.config import TrialConfig
from authark.infrastructure.config.registry import MemoryRegistry
from authark.infrastructure.config.context import Context


@fixture
def config():
    return TrialConfig()


@fixture
def registry(config):
    return MemoryRegistry(config)


@fixture
def context(config, registry):
    return Context(config, registry)
