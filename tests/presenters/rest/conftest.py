from pytest import fixture
from injectark import Injectark
from authark.core import config
from authark.factories import strategy_builder, factory_builder
from authark.presenters.rest import RestApplication


@fixture
def app(loop, aiohttp_client):
    config['factory'] = 'CheckFactory'
    config['strategies'] = ['base', 'check']
    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    injector = Injectark(factory, strategy)

    rest = RestApplication(config, injector)

    return loop.run_until_complete(aiohttp_client(rest.app))


@fixture
def headers() -> dict:
    return {
        "From": "john@doe.com",
        "TenantId": "001",
        "UserId": "001",
        "Roles": "user"
    }
