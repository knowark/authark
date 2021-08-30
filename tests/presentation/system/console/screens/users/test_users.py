
import asyncio
from types import MethodType
from pytest import fixture, mark
from widark import Event
from authark.presentation.system.console.screens.users.users import (
    UsersScreen, UserDetailsModal)

pytestmark = mark.asyncio


@fixture
def users_screen(root, injector):
    return UsersScreen(root, injector=injector)


@fixture
def user_details_modal(root, injector):
    user = {'id': '1', 'name': 'John Doe', 'username': 'doe',
            'email': '', 'attributes': {}}
    return UserDetailsModal(root, injector=injector, user=user)


async def test_users_screen_instantiation_defaults(users_screen):
    assert users_screen.user is None


async def test_users_screen_load(users_screen):
    await users_screen.load()
    await asyncio.sleep(0)

    assert len(users_screen.body.data) == 2


async def test_users_screen_on_body(users_screen):
    def target(item_):
        class MockTarget:
            class parent:
                item = item_
        return MockTarget()

    event = Event('Mouse', 'click')
    event.target = target(None)

    await users_screen.on_body(event)
    assert users_screen.modal is None

    event.target = target(
        {'id': '1',  'name': '', 'username': '',
         'email': '', 'attributes': {}})

    await users_screen.on_body(event)
    await asyncio.sleep(0)

    assert users_screen.modal is not None


async def test_users_screen_on_create(users_screen):
    event = Event('Mouse', 'click')
    await users_screen.on_create(event)
    await asyncio.sleep(0)
    assert users_screen.modal.user == {'name': '', 'username': '',
                                       'email': '', 'attributes': {}}


async def test_users_screen_on_search(users_screen):
    focus_called = False

    class MockSearch:
        text = 'value'

        def focus(self):
            nonlocal focus_called
            focus_called = True

    users_screen.search = MockSearch()

    await users_screen.on_search(Event('Keyboard', 'keydown', key='value'))
    assert users_screen.domain == []

    await users_screen.on_search(Event('Keyboard', 'keydown', key='\n'))

    await asyncio.sleep(0)
    assert focus_called is True
    assert users_screen.domain == [
        '|', ('name', 'ilike', '%value%'), ('email', 'ilike', '%value%')]


async def test_users_screen_on_modal_done(users_screen):
    event = Event('Custom', 'done', details={'result': 'roles'})
    await users_screen.on_modal_done(event)

    assert type(users_screen.modal).__name__ == 'RankingsModal'

    event = Event('Custom', 'done', details={'result': 'credentials'})
    await users_screen.on_modal_done(event)

    assert type(users_screen.modal).__name__ == 'CredentialsModal'

    event = Event('Custom', 'done', details={'result': 'other'})
    await users_screen.on_modal_done(event)
    await asyncio.sleep(0)

    assert len(users_screen.body.data) == 2


async def test_users_details_modal_on_save(user_details_modal):
    event = Event('Mouse', 'click')

    given_users = None

    async def mock_update(self, users):
        nonlocal given_users
        given_users = users

    user_details_modal.build()
    user_details_modal.procedure_manager.update = MethodType(
        mock_update, user_details_modal)

    await user_details_modal.on_save(event)

    assert given_users == [{'id': '1', 'attributes': {}, 'email': '',
                            'name': 'John Doe', 'username': 'doe'}]

    class MockPassword:
        text = 'SECRET'

    user_details_modal.password = MockPassword()
    await user_details_modal.on_save(event)
    await asyncio.sleep(0)

    assert given_users == [{'id': '1', 'attributes': {}, 'email': '',
                            'name': 'John Doe', 'username': 'doe',
                            'password': 'SECRET'}]


async def test_users_details_modal_on_buttons(user_details_modal):
    event = Event('Mouse', 'click')
    given_result = None

    async def mock_done(self, result):
        nonlocal given_result
        given_result = result

    user_details_modal.done = MethodType(mock_done, user_details_modal)

    await user_details_modal.on_cancel(event)
    assert given_result == {'result': 'cancelled'}

    await user_details_modal.on_delete(event)
    assert given_result == {'result': 'deleted'}

    await user_details_modal.on_roles(event)
    assert given_result == {'result': 'roles'}

    await user_details_modal.on_credentials(event)
    await asyncio.sleep(0)
    assert given_result == {'result': 'credentials'}
