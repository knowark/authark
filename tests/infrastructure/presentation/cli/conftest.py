from pytest import fixture
from injectark import Injectark, Factory
from authark.infrastructure.config import DEVELOPMENT_CONFIG
from authark.infrastructure.cli import Cli
from authark.infrastructure.factories import (
    factory_builder, strategy_builder)


@fixture
def mock_config():
    return DEVELOPMENT_CONFIG


@fixture
def mock_factory(mock_config):
    factory = factory_builder.build(mock_config)
    called = False

    class MockWebApplication:
        async def run(self):
            nonlocal called
            called = True

    def web_application():
        return

    factory.web_application = web_application

    return called is True


@fixture
def mock_strategy(mock_config):
    return strategy_builder.build(mock_config['strategies'])


@fixture
def mock_injector(mock_strategy, mock_factory):
    return Injectark(mock_strategy, mock_factory)


@fixture
def cli(mock_config, mock_injector) -> Cli:
    return Cli(mock_config, mock_injector)
