
import asyncio
from types import MethodType
from pytest import fixture, mark
from widark import Event
from authark.presentation.system.console.screens.status import (
    StatusScreen, TenantsModal, TenantProvisionModal)

pytestmark = mark.asyncio


@fixture
def status_screen(root, injector):
    return StatusScreen(root, injector=injector)


@fixture
def tenants_modal(root, injector):
    return TenantsModal(root, injector=injector)


@fixture
def tenant_provision_modal(root, injector):
    return TenantProvisionModal(root, injector=injector)


async def test_status_screen_load(status_screen):
    await status_screen.load()
    await asyncio.sleep(0)

    assert status_screen.tenant_name.content == 'Default'
    assert status_screen.tenant_slug.content == 'default'


async def test_status_screen_on_create(status_screen):
    event = Event('Mouse', 'click')
    await status_screen.on_switch(event)
    await asyncio.sleep(0)

    assert type(status_screen.modal).__name__ == 'TenantsModal'


async def test_status_screen_on_provision(status_screen):
    event = Event('Mouse', 'click')
    await status_screen.on_provision(event)
    await asyncio.sleep(0)

    assert type(status_screen.modal).__name__ == 'TenantProvisionModal'


async def test_status_screen_on_modal_done(status_screen):
    event = Event('Custom', 'done', details={'result': 'roles'})
    await status_screen.on_modal_done(event)

    assert status_screen.modal is None


async def test_status_screen_on_switch(status_screen):
    await status_screen.on_switch(Event('Mouse', 'click'))

    assert type(status_screen.modal).__name__ == 'TenantsModal'


async def test_tenants_modal_on_body(tenants_modal):
    given_details = None

    async def mock_done(self, details):
        nonlocal given_details
        given_details = details

    tenants_modal.connect()
    tenants_modal.done = MethodType(mock_done, tenants_modal)

    def target(item_):
        class MockTarget:
            class parent:
                item = item_
        return MockTarget()

    event = Event('Mouse', 'click')
    event.target = target({'id': '1', 'name': 'Company'})

    await tenants_modal.on_body(event)
    await asyncio.sleep(0)

    assert given_details == {'id': '1', 'name': 'Company'}


async def test_provision_modal_on_save(tenant_provision_modal):
    event = Event('Mouse', 'click')

    given_tenants = None

    def mock_create_tenant(self, tenants):
        nonlocal given_tenants
        given_tenants = tenants

    tenant_provision_modal.build()
    tenant_provision_modal.tenant_supplier.create_tenant = MethodType(
        mock_create_tenant, tenant_provision_modal)

    await tenant_provision_modal.on_save(event)

    assert given_tenants == {'name': ''}

    class MockId:
        text = '123'

    tenant_provision_modal.id = MockId()
    await tenant_provision_modal.on_save(event)
    await asyncio.sleep(0)

    assert given_tenants == {'id': '123', 'name': ''}


async def test_tenant_provision_modal_on_buttons(tenant_provision_modal):
    event = Event('Mouse', 'click')
    given_result = None

    async def mock_done(self, result):
        nonlocal given_result
        given_result = result

    tenant_provision_modal.done = MethodType(mock_done, tenant_provision_modal)

    await tenant_provision_modal.on_cancel(event)
    assert given_result == {'result': 'cancelled'}
