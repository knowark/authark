import urwid
from pytest import raises, fixture
from authark.infrastructure.terminal.screens.users import (
    UsersScreen, UsersAddScreen, UsersDeleteScreen, UsersCredentialsScreen)
from authark.infrastructure.terminal.screens.users.users_roles import (
    UsersRolesScreen)
from authark.infrastructure.terminal.screens.users.users_actions import (
    UsersUpdateScreen)
from authark.infrastructure.terminal.screens.users.users_roles import (
    UsersRolesScreen)


@fixture
def users_screen(main):
    return UsersScreen('USERS', main.env)


def test_users_screen_instantiation(users_screen):
    assert users_screen is not None


def test_users_on_search_user(users_screen):
    users_screen.on_search_user(None, "domain")
    assert users_screen.table.data_list == []


def test_users_show_roles_screen(users_screen):
    users_screen.show_roles_screen()
    assert isinstance(
        users_screen.env.holder.original_widget, UsersRolesScreen)


def test_users_screen_keypress(users_screen):
    users_screen.pile.focus_position = 1
    users_screen.keypress(None, 'A')
    assert isinstance(
        users_screen.env.holder.original_widget, UsersAddScreen)
    users_screen.keypress(None, 'D')
    assert isinstance(
        users_screen.env.holder.original_widget, UsersDeleteScreen)
    users_screen.keypress(None, 'C')
    assert isinstance(
        users_screen.env.holder.original_widget, UsersCredentialsScreen)
    users_screen.keypress(None, 'U')
    assert isinstance(
        users_screen.env.holder.original_widget, UsersUpdateScreen)
    users_screen.keypress(None, 'R')
    assert isinstance(
        users_screen.env.holder.original_widget, UsersRolesScreen)
    users_screen.pile._selectable = False
    unhandled = users_screen.keypress((40, 40), 'F')
    assert unhandled == 'F'


def test_users_screen_keypress_focus_out(users_screen):
    with raises(TypeError):
        users_screen.keypress(None, 'down')


def test_users_screen_on_search_user_no_users(users_screen):
    users_screen.on_search_user(None, "")
    assert len(users_screen.table.data_list) == 1
