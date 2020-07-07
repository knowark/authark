
import asyncio
from types import MethodType
from pytest import fixture, mark
from widark import Event
from authark.presenters.console.screens.roles.roles import (
    RolesScreen, RoleDetailsModal, UsersSelectionModal, DominionsModal)

pytestmark = mark.asyncio


@fixture
def roles_screen(root, injector):
    dominion = {'id': '1', 'name': 'Proser'}
    return RolesScreen(root, injector=injector, dominion=dominion)


@fixture
def role_details_modal(root, injector):
    role = {'id': '1', 'name': 'admin', 'dominion_id': '1', 'description': ''}
    return RoleDetailsModal(root, injector=injector, role=role)


@fixture
def dominions_modal(root, injector):
    return DominionsModal(root, injector=injector)


@fixture
def users_selection_modal(root, injector):
    role = {'id': '1', 'name': 'admin', 'dominion_id': '1', 'description': ''}
    return UsersSelectionModal(root, injector=injector, role=role)


async def test_roles_instantiation_defaults(roles_screen):
    assert roles_screen.dominion == {}


async def test_roles_screen_load(roles_screen):
    roles_screen.build()
    await roles_screen.load()
    await asyncio.sleep(0)

    assert len(roles_screen.body.data) == 1


async def test_roles_screen_on_modal_done(roles_screen):
    event = Event('Custom', 'done', details={'result': 'default'})
    await roles_screen.on_modal_done(event)
    await asyncio.sleep(0)

    assert roles_screen.modal is None
    assert len(roles_screen.body.data) == 1


async def test_roles_screen_on_dominion(roles_screen):
    event = Event('Custom', 'done', details={'result': 'default'})
    await roles_screen.on_dominion(event)
    await asyncio.sleep(0)

    assert type(roles_screen.modal).__name__ == 'DominionsModal'


async def test_roles_screen_on_dominion_switch(roles_screen):
    event = Event('Custom', 'done', details={'id': '1', 'name': 'Dominion'})
    await roles_screen.on_dominion_switch(event)
    await asyncio.sleep(0)

    assert roles_screen.dominion == {'id': '1', 'name': 'Dominion'}


async def test_roles_screen_on_body(roles_screen):
    def target(item_):
        class MockTarget:
            class parent:
                item = item_
        return MockTarget()

    event = Event('Mouse', 'click')
    event.target = target(None)

    await roles_screen.on_body(event)
    assert roles_screen.modal is None

    event.target = target({'id': '1', 'name': 'admin',
                           'dominion_id': '1', 'description': ''})

    await roles_screen.on_body(event)
    await asyncio.sleep(0)

    assert roles_screen.modal is not None


async def test_roles_screen_on_create(roles_screen):
    event = Event('Mouse', 'click')
    await roles_screen.on_create(event)
    await asyncio.sleep(0)
    assert roles_screen.modal.role == {
        'name': '', 'description': '', 'dominion_id': None, 'id': ''}


async def test_roles_screen_on_modal_done(roles_screen):
    roles_screen.role = {'id': '1', 'name': 'admin',
                         'dominion_id': '1', 'description': ''}
    event = Event('Custom', 'done', details={'result': 'policies'})
    roles_screen.build()
    await roles_screen.load()
    await roles_screen.on_modal_done(event)

    assert type(roles_screen.modal).__name__ == 'PoliciesModal'

    event = Event('Custom', 'done', details={'result': 'other'})
    await roles_screen.on_modal_done(event)

    assert len(roles_screen.body.data) == 1

    event = Event('Custom', 'done', details={'result': 'users'})
    await roles_screen.on_modal_done(event)
    await asyncio.sleep(0)

    assert type(roles_screen.modal).__name__ == 'UsersSelectionModal'


async def test_roles_screen_on_cancel(roles_screen):
    event = Event('Mouse', 'click')
    given_result = None

    async def mock_done(self, result):
        nonlocal given_result
        given_result = result

    roles_screen.done = MethodType(mock_done, roles_screen)

    await roles_screen.on_cancel(event)
    assert given_result == {'result': 'cancelled'}


async def test_dominions_modal_on_body(dominions_modal):
    given_details = None

    async def mock_done(self, details):
        nonlocal given_details
        given_details = details

    dominions_modal.connect()
    dominions_modal.done = MethodType(mock_done, dominions_modal)

    def target(item_):
        class MockTarget:
            class parent:
                item = item_
        return MockTarget()

    event = Event('Mouse', 'click')
    event.target = target({'id': '1', 'name': 'Dominion'})

    await dominions_modal.on_body(event)
    await asyncio.sleep(0)

    assert given_details == {'id': '1', 'name': 'Dominion'}


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

    role_details_modal.build()
    role_details_modal.management_manager.create_role = MethodType(
        create_role, role_details_modal)

    await role_details_modal.on_save(event)
    await asyncio.sleep(0)

    assert given_roles == [{'description': '', 'dominion_id': '1',
                            'id': '1', 'name': 'admin'}]


async def test_users_selection_modal_on_select(users_selection_modal):
    def target(item_):
        class MockTarget:
            class parent:
                item = item_

            def focus(self):
                pass
        return MockTarget()

    users_selection_modal.connect()
    event = Event('Mouse', 'click')
    event.target = target({'id': '1', 'username': 'eecheverry',
                           'email': 'eecheverry@knowark.com1'})

    await users_selection_modal.on_select(event)
    await asyncio.sleep(0)

    assert users_selection_modal.focused == {
        'id': '1', 'username': 'eecheverry',
        'email': 'eecheverry@knowark.com1'}


async def test_users_selection_modal_on_available_search(users_selection_modal):
    users_selection_modal.build()
    users_selection_modal.available_search.setup(content='value').connect()

    assert users_selection_modal.available_search.text == 'value'
    assert users_selection_modal.available_domain == []

    await users_selection_modal.on_available_search(
        Event('Keyboard', 'keydown', key=''))
    await users_selection_modal.on_available_search(
        Event('Keyboard', 'keydown', key='\n'))

    await asyncio.sleep(0)
    assert users_selection_modal.available_domain == [
        '|', ('name', 'ilike', '%value%'), ('email', 'ilike', '%value%')]


async def test_users_selection_modal_on_chosen_search(users_selection_modal):
    users_selection_modal.build()
    users_selection_modal.chosen_search.setup(content='value').connect()

    assert users_selection_modal.chosen_search.text == 'value'
    assert users_selection_modal.chosen_domain == []

    await users_selection_modal.on_chosen_search(
        Event('Keyboard', 'keydown', key=''))
    await users_selection_modal.on_chosen_search(
        Event('Keyboard', 'keydown', key='\n'))

    await asyncio.sleep(0)
    assert users_selection_modal.chosen_domain == [
        '|', ('name', 'ilike', '%value%'), ('email', 'ilike', '%value%')]


async def test_users_selection_modal_on_choose(users_selection_modal):
    users_selection_modal.build()
    users_selection_modal.chosen_search.setup(content='value').connect()

    await users_selection_modal.on_choose(Event('Mouse', 'click'))
    assert users_selection_modal.available.data == []

    item = {'id': '1', 'usename': 'Dummy'}
    users_selection_modal.focused = item
    users_selection_modal.available.data = [item]

    await users_selection_modal.on_choose(Event('Mouse', 'click'))
    await asyncio.sleep(0)

    assert users_selection_modal.available.data == []
    assert users_selection_modal.chosen.data == [item]


async def test_users_selection_modal_on_choose_all(users_selection_modal):
    users_selection_modal.build()
    users_selection_modal.chosen_search.setup(content='value').connect()

    item_1 = {'id': '1', 'usename': 'Dummy 1'}
    item_2 = {'id': '2', 'usename': 'Dummy 2'}

    users_selection_modal.available.data = [item_1, item_2]

    await users_selection_modal.on_choose_all(Event('Mouse', 'click'))
    await asyncio.sleep(0)

    assert users_selection_modal.available.data == []
    assert users_selection_modal.chosen.data == [item_1, item_2]


async def test_users_selection_modal_on_clear(users_selection_modal):
    users_selection_modal.build()
    users_selection_modal.chosen_search.setup(content='value').connect()

    item = {'id': '1', 'usename': 'Dummy'}
    users_selection_modal.focused = item
    users_selection_modal.chosen.data = [item]

    await users_selection_modal.on_clear(Event('Mouse', 'click'))
    await asyncio.sleep(0)

    assert users_selection_modal.chosen.data == []
    assert users_selection_modal.available.data == [item]


async def test_users_selection_modal_on_clear_all(users_selection_modal):
    users_selection_modal.build()
    users_selection_modal.chosen_search.setup(content='value').connect()

    item_1 = {'id': '1', 'usename': 'Dummy 1'}
    item_2 = {'id': '2', 'usename': 'Dummy 2'}
    users_selection_modal.chosen.data = [item_1, item_2]

    await users_selection_modal.on_clear_all(Event('Mouse', 'click'))
    await asyncio.sleep(0)

    assert users_selection_modal.chosen.data == []
    assert users_selection_modal.available.data == [item_1, item_2]


async def test_users_selection_modal_on_cancel(users_selection_modal):
    event = Event('Mouse', 'click')
    given_result = None

    async def mock_done(self, result):
        nonlocal given_result
        given_result = result

    users_selection_modal.done = MethodType(mock_done, users_selection_modal)

    await users_selection_modal.on_cancel(event)
    assert given_result == {'result': 'cancelled'}


async def test_users_selection_modal_on_save(users_selection_modal):
    event = Event('Mouse', 'click')

    given_ranking_ids = None

    async def deassign_role(self, ranking_ids):
        nonlocal given_ranking_ids
        given_ranking_ids = ranking_ids

    users_selection_modal.build()
    users_selection_modal.management_manager.deassign_role = MethodType(
        deassign_role, users_selection_modal)

    await users_selection_modal.on_save(event)
    await asyncio.sleep(0)

    assert given_ranking_ids == []
