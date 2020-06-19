import asyncio
from types import MethodType
from pytest import fixture, mark
from widark import Application, Event
from authark.presenters.console import ConsoleApplication

pytestmark = mark.asyncio


@fixture
def application(root, config, injector):
    return ConsoleApplication(config=config, injector=injector)


async def test_application_instantiation_defaults(application):
    assert isinstance(application, Application)


async def test_application_build(application):
    application.build()
    assert application.body is not None


async def test_application_prepare(application):
    given_tenant = None

    def mock_set_tenant(self, tenant):
        nonlocal given_tenant
        given_tenant = tenant

    application.session_manager.set_tenant = MethodType(
        mock_set_tenant, application.session_manager)

    await application.prepare()
    await asyncio.sleep(0)

    assert given_tenant is not None


async def test_application_on_menu_click(application):
    def target(item_):
        class MockTarget:
            class parent:
                item = item_
        return MockTarget()

    event = Event('Mouse', 'click')

    application.build()

    event.target = target({'tag': 'users'})
    await application.on_menu_click(event)
    await asyncio.sleep(0)

    assert type(application.body.children[0]).__name__ == 'UsersScreen'

    event.target = target({'tag': 'dominions'})
    await application.on_menu_click(event)
    await asyncio.sleep(1 / 15)

    assert type(application.body.children[0]).__name__ == 'DominionsScreen'

    event.target = target({'tag': 'other'})
    await application.on_menu_click(event)
    assert type(application.body.children[0]).__name__ == 'DominionsScreen'


async def test_application_on_tenant_switch(application):
    given_tenant = None

    def mock_set_tenant(self, tenant):
        nonlocal given_tenant
        given_tenant = tenant

    application.session_manager.set_tenant = MethodType(
        mock_set_tenant, application.session_manager)

    event = Event('Mouse', 'click')
    await application.on_tenant_switch(event)
    await asyncio.sleep(0)

    assert given_tenant is None

    event = Event('Mouse', 'click', details={'name': 'Corporation X'})
    await application.on_tenant_switch(event)
    await asyncio.sleep(0)

    assert given_tenant is not None
