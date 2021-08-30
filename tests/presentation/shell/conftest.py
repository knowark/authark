from pytest import fixture
from injectark import Injectark
from authark.integration.core import config
from authark.presentation.shell import Shell
from authark.integration.factories import factory_builder


@fixture
def shell() -> Shell:
    config['factory'] = 'CheckFactory'
    factory = factory_builder.build(config)

    injector = Injectark(factory)

    return Shell(config, injector)
