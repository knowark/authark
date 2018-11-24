from pytest import fixture
from authark.application.models import User, Dominion, Role
from authark.infrastructure.terminal.main import Main
from authark.infrastructure.config.config import TrialConfig
from authark.infrastructure.config.registry import MemoryRegistry
from authark.infrastructure.config.context import Context


@fixture
def context():
    config = TrialConfig()
    registry = MemoryRegistry(config)
    registry['auth_reporter'].user_repository.load({
        "1": User(id='1', username='eecheverry',
                  email='eecheverry@example.com')
    })
    registry['auth_reporter'].dominion_repository.load({
        "1": Dominion(id='1', name='Data Server',
                      url='https://dataserver.nubark.cloud')
    })
    registry['auth_reporter'].role_repository.load({
        "1": Role(id='1', name='manager', dominion_id='1',
                  description='Production Manager')
    })

    return Context(config, registry)


@fixture
def main(context):
    return Main(context)
