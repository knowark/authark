from pytest import fixture
from injectark import Injectark
from authark.infrastructure.core import DEVELOPMENT_CONFIG
from authark.infrastructure.presenters.shell import Shell
from authark.infrastructure.factories import (
    factory_builder, strategy_builder)


@fixture
def shell() -> Shell:
    config = DEVELOPMENT_CONFIG
    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    injector = Injectark(strategy, factory)

    return Shell(config, injector)
