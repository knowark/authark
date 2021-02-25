from pytest import fixture
from injectark import Injectark
from authark.core import config
from authark.presenters.shell import Shell
from authark.factories import factory_builder


@fixture
def shell() -> Shell:
    config['factory'] = 'CheckFactory'
    factory = factory_builder.build(config)

    injector = Injectark(factory)

    return Shell(config, injector)
