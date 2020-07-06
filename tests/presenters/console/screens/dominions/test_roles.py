
import asyncio
from types import MethodType
from pytest import fixture, mark
from widark import Event
from authark.presenters.console.screens.dominions.roles import (
    RolesModal, RoleDetailsModal, UsersSelectionModal)

pytestmark = mark.asyncio


@fixture
def roles_modal(root, injector):
    dominion = {'id': '1', 'name': 'Proser'}
    return RolesModal(root, injector=injector, dominion=dominion)


@fixture
def role_details_modal(root, injector):
    role = {'id': '1', 'name': 'admin', 'dominion_id': '1', 'description': ''}
    return RoleDetailsModal(root, injector=injector, role=role)


@fixture
def users_selection_modal(root, injector):
    role = {'id': '1', 'name': 'admin', 'dominion_id': '1', 'description': ''}
    return UsersSelectionModal(root, injector=injector, role=role)


async def test_roles_instantiation_defaults(roles_modal):
    assert roles_modal.dominion == {'id': '1', 'name': 'Proser'}


async def test_roles_modal_load(roles_modal):
    await roles_modal.load()
    await asyncio.sleep(0)

    assert len(roles_modal.body.data) == 1


async def test_roles_modal_on_modal_done(roles_modal):
    event = Event('Custom', 'done', details={'result': 'default'})
    await roles_modal.on_modal_done(event)
    await asyncio.sleep(0)

    assert roles_modal.modal is None
    assert len(roles_modal.body.data) == 1


async def test_roles_modal_on_body(roles_modal):
    def target(item_):
        class MockTarget:
            class parent:
                item = item_
        return MockTarget()

    event = Event('Mouse', 'click')
    event.target = target(None)

    await roles_modal.on_body(event)
    assert roles_modal.modal is None

    event.target = target({'id': '1', 'name': 'admin',
                           'dominion_id': '1', 'description': ''})

    await roles_modal.on_body(event)
    await asyncio.sleep(0)

    assert roles_modal.modal is not None


async def test_roles_modal_on_create(roles_modal):
    event = Event('Mouse', 'click')
    await roles_modal.on_create(event)
    await asyncio.sleep(0)
    assert roles_modal.modal.role == {
        'name': '', 'description': '', 'dominion_id': '1', 'id': ''}


async def test_roles_modal_on_modal_done(roles_modal):
    roles_modal.role = {'id': '1', 'name': 'admin',
                        'dominion_id': '1', 'description': ''}
    event = Event('Custom', 'done', details={'result': 'policies'})
    await roles_modal.on_modal_done(event)

    assert type(roles_modal.modal).__name__ == 'PoliciesModal'

    event = Event('Custom', 'done', details={'result': 'other'})
    await roles_modal.on_modal_done(event)

    assert len(roles_modal.body.data) == 1

    event = Event('Custom', 'done', details={'result': 'users'})
    await roles_modal.on_modal_done(event)
    await asyncio.sleep(0)

    assert type(roles_modal.modal).__name__ == 'UsersSelectionModal'


async def test_roles_modal_on_cancel(roles_modal):
    event = Event('Mouse', 'click')
    given_result = None

    async def mock_done(self, result):
        nonlocal given_result
        given_result = result

    roles_modal.done = MethodType(mock_done, roles_modal)

    await roles_modal.on_cancel(event)
    assert given_result == {'result': 'cancelled'}


async def test_role_details_modal_on_buttons(role_details_modal):
    event = Event('Mouse', 'click')
    given_result = None

    async def mock_done(self, result):
        nonlocal given_result
        given_result = result

    role_details_modal.done = MethodType(mock_done, role_details_modal)

    await role_details_modal.on_cancel(event)
    assert given_result == {'result': 'cancelled'}

    await role_details_modal.on_delete(event)
    assert given_result == {'result': 'deleted'}

    await role_details_modal.on_policies(event)
    assert given_result == {'result': 'policies'}

    await role_details_modal.on_users(event)
    assert given_result == {'result': 'users'}


async def test_role_details_modal_on_save(role_details_modal):
    event = Event('Mouse', 'click')

    given_roles = None

    async def create_role(self, roles):
        nonlocal given_roles
        given_roles = roles

    role_details_modal.management_manager.create_role = MethodType(
        create_role, role_details_modal)

    await role_details_modal.on_save(event)
    await asyncio.sleep(0)

    assert given_roles == [{'description': '', 'dominion_id': '1',
                            'id': '1', 'name': 'admin'}]


async def test_users_selection_modall_on_select(users_selection_modal):
    def target(item_):
        class MockTarget:
            class parent:
                item = item_
        return MockTarget()

    assert len(users_selection_modal.available.data) == 0
    assert len(users_selection_modal.chosen.data) == 0

    event = Event('Mouse', 'click')
    event.target = target({'id': '1', 'name': 'admin',
                           'dominion_id': '1', 'description': ''})

    await users_selection_modal.on_select(event)
    await asyncio.sleep(0)

    assert len(users_selection_modal.available.data) == 0
    assert len(users_selection_modal.chosen.data) == 1
