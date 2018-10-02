import urwid
from pytest import raises, fixture
from authark.infrastructure.terminal.screens.users.users import UsersScreen
from authark.infrastructure.terminal.screens.users.users_actions import (
    UsersAddScreen, UsersDeleteScreen, UsersCredentialsScreen)


@fixture
def users_screen(main):
    return UsersScreen('USERS', main.env)


def test_users_screen_instantiation(users_screen):
    assert users_screen is not None


def test_users_screen_keypress(users_screen):
    users_screen.table.keypress(None, 'down')
    users_screen.keypress(None, 'A')
    focused_widget = users_screen.env.holder.original_widget
    assert isinstance(focused_widget, UsersAddScreen)
    users_screen.keypress(None, 'D')
    focused_widget = users_screen.env.holder.original_widget
    assert isinstance(focused_widget, UsersDeleteScreen)
    users_screen.keypress(None, 'C')
    focused_widget = users_screen.env.holder.original_widget
    assert isinstance(focused_widget, UsersCredentialsScreen)
    unhandled = users_screen.keypress((40, 40), 'F')
    assert unhandled == 'F'
