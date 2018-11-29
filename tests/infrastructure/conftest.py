from pytest import fixture
from authark.infrastructure.config import TrialConfig
from authark.infrastructure.resolver import Resolver


@fixture
def config():
    return TrialConfig()


@fixture
def registry(config):
    resolver = Resolver(config)
    return resolver.resolve(config['providers'])


@fixture
def context(config, registry):
    return Context(config, registry)
