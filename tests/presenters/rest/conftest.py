from pytest import fixture
from injectark import Injectark
from authark.core import config
from authark.factories import factory_builder
from authark.presenters.rest import RestApplication


@fixture
def app(loop, aiohttp_client):
    config['factory'] = 'CheckFactory'
    factory = factory_builder.build(config)

    injector = Injectark(factory)

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
