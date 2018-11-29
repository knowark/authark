from pytest import fixture
from authark.application.models import User, Dominion, Role
from authark.infrastructure.terminal.main import Main
from authark.infrastructure.config import TrialConfig
from authark.infrastructure.resolver import Resolver
from authark.infrastructure.terminal.framework import Context


@fixture
def context():
    config = TrialConfig()
    resolver = Resolver(config)
    registry = resolver.resolve(config['providers'])

    registry['AutharkReporter'].user_repository.load({
        "1": User(id='1', username='eecheverry',
                  email='eecheverry@example.com')
    })
    registry['AutharkReporter'].dominion_repository.load({
        "1": Dominion(id='1', name='Data Server',
                      url='https://dataserver.nubark.cloud')
    })
    registry['AutharkReporter'].role_repository.load({
        "1": Role(id='1', name='manager', dominion_id='1',
                  description='Production Manager')
    })

    return Context(config, registry)


@fixture
def main(context):
    return Main(context)
