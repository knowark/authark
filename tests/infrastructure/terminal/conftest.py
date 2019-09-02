from pytest import fixture
from injectark import Injectark
from authark.application.models import (
    User, Dominion, Role, Policy, Permission, Resource)
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

    tenant = Tenant(id='1', name='Knowark')
    resolver['TenantSupplier'].arranger.cataloguer.catalog = {
        "1": tenant
    }
    resolver['AutharkReporter'].user_repository.load({
        "knowark": {
            "1": User(id='1', username='eecheverry',
                      email='eecheverry@example.com')
        }
    })
    resolver['AutharkReporter'].dominion_repository.load({
        "knowark": {
            "1": Dominion(id='1', name='Data Server',
                          url='https://dataserver.nubark.cloud')
        }
    })
    resolver['AutharkReporter'].role_repository.load({
        "knowark": {
            "1": Role(id='1', name='manager', dominion_id='1',
                      description='Production Manager')
        }
    })
    resolver['ComposingReporter'].policy_repository.load({
        "knowark": {
            "1": Policy(id='1', type='string', name='Function access',
                        value="enabled")
        }
    })
    resolver['ComposingReporter'].permission_repository.load({
        "knowark": {
            "1": Permission(id='1', policy_id='1', resource_id='1')
        }
    })
    resolver['ComposingReporter'].resource_repository.load({
        "knowark": {
            "1": Resource(id='1', name='resource', dominion_id='1')
        }
    })
    resolver['SessionCoordinator'].tenant_provider.setup(tenant)

    return Context(config, resolver)


@fixture
def main(context):
    return Main(context)
