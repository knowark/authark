import urwid
from pytest import raises, fixture
from authark.infrastructure.terminal.screens.users import (
    UsersScreen, UsersAddScreen, UsersDeleteScreen, UsersCredentialsScreen)
from authark.infrastructure.terminal.screens.users.users_roles import (
    UsersRolesScreen, UsersAssignRoleScreen, UsersDeassignRoleScreen)
from authark.infrastructure.terminal.screens.users.users_actions import (
    UsersUpdateScreen)


@fixture
def users_roles_screen(main):
    users_screen = UsersScreen('USERS', main.env)
    users_screen.pile.focus_position = 1
    users_screen.keypress((0, 0), 'R')
    users_roles_screen = users_screen.env.holder.original_widget
    assert isinstance(users_roles_screen, UsersRolesScreen)
    unhandled = users_roles_screen.keypress((40, 40), 'F')
    assert unhandled == 'F'

    return users_roles_screen


@fixture
def users_assign_role_screen(users_roles_screen):
    users_roles_screen.keypress((0, 0), 'A')
    users_assign_role_screen = users_roles_screen.env.holder.original_widget
    assert isinstance(users_assign_role_screen, UsersAssignRoleScreen)
    return users_assign_role_screen


@fixture
def users_deassign_role_screen(users_roles_screen):
    users_roles_screen.keypress((0, 0), 'D')
    users_deassign_role_screen = users_roles_screen.env.holder.original_widget
    assert isinstance(users_deassign_role_screen, UsersDeassignRoleScreen)
    return users_deassign_role_screen


def test_users_roles_screen_no_parent(main):
    assert UsersRolesScreen("USER'S ROLES", main.env) is not None


def test_users_assign_role_screen_no_parent(main):
    assert UsersAssignRoleScreen("ASSIGN ROLE", main.env) is not None


def test_users_deassign_role_screen_no_parent(main):
    assert UsersDeassignRoleScreen("DEASSIGN ROLE", main.env) is not None


def test_users_roles_screen_instance(users_roles_screen):
    assert users_roles_screen is not None


def test_users_assign_role_screen_instance(users_assign_role_screen):
    assert users_assign_role_screen is not None


def test_users_assign_role_screen_dominion_selection(users_assign_role_screen):
    build_dominion_selection = \
        users_assign_role_screen._build_dominion_selection()
    dominions = build_dominion_selection.item_list_collector("")
    assert dominions[0]["id"] == '1'
    name = build_dominion_selection.item_formatter({'name': 'Jhon Jairo'})
    assert name == "Jhon Jairo"


def test_users_assign_role_screen_role_selection(users_assign_role_screen):
    build_role_selection = \
        users_assign_role_screen._build_role_selection()
    assert len(build_role_selection.item_list_collector("")) == 0
    users_assign_role_screen.dominion_selection.selected = {'id': '1'}
    assert len(build_role_selection.item_list_collector("")) == 1
    name = build_role_selection.item_formatter({'name': 'Jhon Jairo'})
    assert name == "Jhon Jairo"


def test_users_assign_role_screen_add_ranking(users_assign_role_screen):
    users_assign_role_screen._add_ranking(None)
    assert isinstance(users_assign_role_screen.env.holder.original_widget,
                      UsersAssignRoleScreen)
    users_assign_role_screen.user = {'id': '1'}
    users_assign_role_screen.role_selection.selected = {'id': '1'}
    users_assign_role_screen._add_ranking(None)
    assert isinstance(users_assign_role_screen.env.holder.original_widget,
                      UsersRolesScreen)


def test_users_deassign_role_screen_instance(users_deassign_role_screen):
    assert users_deassign_role_screen is not None


def test_users_deassign_role_keypress(users_deassign_role_screen):
    users_deassign_role_screen.keypress((0, 0), "enter")
    assert isinstance(users_deassign_role_screen.env.holder.original_widget,
                      UsersRolesScreen)


def test_users_deassign_role_go_back(users_deassign_role_screen):
    users_deassign_role_screen._go_back()
    assert isinstance(users_deassign_role_screen.env.holder.original_widget,
                      UsersRolesScreen)
