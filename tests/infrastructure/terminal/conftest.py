from pytest import fixture
from authark.infrastructure.terminal.main import Main
from authark.infrastructure.config.config import TrialConfig
from authark.infrastructure.config.registry import MemoryRegistry
from authark.infrastructure.config.context import Context


@fixture
def context():
    config = TrialConfig()
    registry = MemoryRegistry(config)
    return Context(config, registry)


@fixture
def main(context):
    return Main(context)
