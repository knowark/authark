from pytest import fixture
from injectark import Injectark
from authark.core import config
from authark.factories import factory_builder
from authark.presenters.rest import RestApplication


@fixture
def app(loop, aiohttp_client):
    config['factory'] = 'CheckFactory'
    config['tokens']['verification']['secret'] = (
        'DEVSECRET123')
    factory = factory_builder.build(config)

    injector = Injectark(factory)

    rest = RestApplication(config, injector)

    return loop.run_until_complete(aiohttp_client(rest.app))


@fixture
def headers() -> dict:
    return {
        "Authorization":  (
            # Password: INTEGRARK_SECRET
            # Payload:
            # {
            #     "tid": "001",
            #     "uid": "001",
            #     "tenant": "Knowark",
            #     "name": "John Doe",
            #     "email": "john@doe.com"
            # }
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0aWQiOiIwMDEiLCJ1aWQiOi"
            "IwMDEiLCJ0ZW5hbnQiOiJLbm93YXJrIiwibmFtZSI6IkpvaG4gRG9lIiwiZW1ha"
            "WwiOiJqb2huQGRvZS5jb20ifQ.udlkUWVOatst5IoDRlJsQVn"
            "U_atCAltOelOJvRCr8BY"
        )

    }
