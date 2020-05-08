from pytest import fixture
from injectark import Injectark
from authark.infrastructure.core import DEVELOPMENT_CONFIG
from authark.infrastructure.factories import (
    strategy_builder, factory_builder)
from authark.infrastructure.presenters.rest import RestApplication


@fixture
def app(loop, aiohttp_client):
    """Create app testing client"""
    config = DEVELOPMENT_CONFIG
    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    injector = Injectark(strategy, factory)

    app = RestApplication(config, injector)

    return loop.run_until_complete(aiohttp_client(app))


@fixture
def headers() -> dict:
    return {
        "From": "john@doe.com",
        "TenantId": "001",
        "UserId": "001",
        "Roles": "user"
    }
