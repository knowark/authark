from pytest import fixture
from aiohttp import web
from injectark import Injectark
from authark.core import DEVELOPMENT_CONFIG
from authark.factories import strategy_builder, factory_builder
from authark.presenters.rest import RestApplication


@fixture
def app(loop, aiohttp_client):
    """Create app testing client"""
    config = DEVELOPMENT_CONFIG
    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    injector = Injectark(strategy, factory)

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
