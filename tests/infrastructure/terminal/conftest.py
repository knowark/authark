from pytest import fixture
from injectark import Injectark
from authark.application.models import User, Dominion, Role
from authark.application.services import Tenant
from authark.infrastructure.terminal.main import Main
from authark.infrastructure.core import TrialConfig, build_factory
from authark.infrastructure.terminal.framework import Context


@fixture
def context():
    config = TrialConfig()
    factory = build_factory(config)
    strategy = config['strategy']

    resolver = Injectark(strategy=strategy, factory=factory)

    resolver.resolve('CatalogService').catalog = {
        "1": Tenant(id='1', name='Knowark')
    }
    resolver.resolve('AutharkReporter').user_repository.load({
        "knowark": {
            "1": User(id='1', username='eecheverry',
                      email='eecheverry@example.com')
        }
    })
    resolver.resolve('AutharkReporter').dominion_repository.load({
        "knowark": {
            "1": Dominion(id='1', name='Data Server',
                          url='https://dataserver.nubark.cloud')
        }
    })
    resolver.resolve('AutharkReporter').role_repository.load({
        "knowark": {
            "1": Role(id='1', name='manager', dominion_id='1',
                      description='Production Manager')
        }
    })

    return Context(config, resolver)


@fixture
def main(context):
    return Main(context)
