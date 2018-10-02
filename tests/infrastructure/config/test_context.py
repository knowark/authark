from authark.infrastructure.config.config import TrialConfig
from authark.infrastructure.config.registry import MemoryRegistry
from authark.infrastructure.config.context import Context


def test_context_instantiation():
    config = TrialConfig()
    registry = MemoryRegistry(config)
    context = Context(config, registry)
    assert context.config == config
    assert context.registry == registry
