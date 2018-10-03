import urwid
from pytest import raises, fixture
from authark.infrastructure.terminal.framework.screen import Screen
from authark.infrastructure.terminal.framework.table import Table
from authark.infrastructure.terminal.screens.users.users import UsersScreen
from authark.infrastructure.terminal.screens.users.users_actions import (
    UsersAddScreen, UsersDeleteScreen, UsersCredentialsScreen)


@fixture
def users_add_screen(main):
    return UsersAddScreen('USERS ADD', main.env)


@fixture
def users_delete_screen(main):
    class MockParent:
        def __init__(self):
            self.table = Table([
                {'id': '1', 'username': 'eecheverry', 'password': '123'}
            ], ['id', 'username', 'password'])
            self.table.keypress(None, 'down')
    return UsersDeleteScreen('USERS DELETE', main.env, MockParent())


def test_users_add_screen_instantiation(users_add_screen):
    assert users_add_screen is not None


def test_users_add_screen_keypress(main, users_add_screen):
    called = False

    class MockMainMenu(Screen):
        def show_users_screen(self):
            nonlocal called
            called = True

        def _build_widget(self):
            pass

    users_add_screen.env.stack = [MockMainMenu(
        'Mock', main.env), urwid.Text('Mock')]
    users_add_screen.username.edit_text = 'jplozano'
    users_add_screen.email.edit_text = 'jplozano@example.com'
    users_add_screen.password.edit_text = '123'

    result = users_add_screen.keypress((40, 40), 'ctrl')
    assert result == 'ctrl'

    users_add_screen.keypress((40, 40), 'enter')

    assert len(users_add_screen.auth_coordinator.user_repository.items) == 2
    assert called


def test_users_delete_screen_instantiation(users_delete_screen):
    assert users_delete_screen is not None


def test_users_delete_screen_keypress(main, users_delete_screen):
    called = False

    class MockMainMenu(Screen):
        def show_users_screen(self):
            nonlocal called
            called = True

        def _build_widget(self):
            pass

    users_delete_screen.env.stack = [MockMainMenu(
        'Mock', main.env), urwid.Text('Mock')]

    result = users_delete_screen.keypress((40, 40), 'ctrl')
    assert result == 'ctrl'

    users_delete_screen.keypress((40, 40), 'enter')

    assert len(users_delete_screen.auth_coordinator
               .user_repository.items) == 0
    assert called
