from pytest import fixture
from injectark import Injectark
from authark.core import config
from authark.presenters.shell import Shell
from authark.factories import factory_builder, strategy_builder


@fixture
def shell() -> Shell:
    config['factory'] = 'CheckFactory'
    config['strategies'] = ['base', 'check']
    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    injector = Injectark(factory, strategy)

    return Shell(config, injector)
