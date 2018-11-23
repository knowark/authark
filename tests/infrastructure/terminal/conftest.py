from pytest import fixture
from authark.application.models.user import User
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
    return Context(config, registry)


@fixture
def main(context):
    return Main(context)
