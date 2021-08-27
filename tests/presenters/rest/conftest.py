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
            # Password: KNOWARK
            # Payload:
            # {
                # "tid": "001",
                # "uid": "001",
                # "organization": "Default",
                # "tenant": "default",
                # "name": "John Doe",
                # "email": "john@doe.com"
            # }
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0aWQiOiIwMDEiLCJ1aWQi"
            "OiIwMDEiLCJvcmdhbml6YXRpb24iOiJEZWZhdWx0IiwidGVuYW50IjoiZGVmY"
            "XVsdCIsIm5hbWUiOiJKb2huIERvZSIsImVtYWlsIjoiam9obkBkb2UuY29tIn"
            "0.dKyIjylPESVk6Msh1z2DRBu9R0Arc0JfZ46iDCpQa0w"
        )

    }
