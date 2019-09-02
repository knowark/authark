import urwid
from pytest import raises, fixture
from authark.infrastructure.terminal.framework import Table, Screen
from authark.infrastructure.terminal.screens.dominions import (
    DominionsScreen, DominionsAddScreen, DominionsRolesScreen,
    DominionsAddRoleScreen)
from authark.infrastructure.terminal.screens.dominions.roles.permissions \
    import PermissionsScreen, AssignPermissionScreen
from uuid import uuid4


class MockParent(Screen):
    def __init__(self):
        self.dominion = {'id': '1', 'name': 'Data Server',
                         'url': 'https://dataserver.nubark.cloud'}
        self.table = Table([
            {'id': '1', 'name': 'admin', 'description': 'Administrator'}
        ], ['id', 'name', 'description'])
        self.table.keypress(None, 'down')


@fixture
def dominions_add_screen(main):
    return DominionsAddScreen('DOMINIONS ADD', main.env)


def test_dominions_add_screen_instantiation(dominions_add_screen):
    assert dominions_add_screen is not None


def test_dominions_roles_screen(main):
    assert DominionsRolesScreen('DOMINION ROLES', main.env, None) is not None


def test_dominions_permisions_screen(main):
    assert PermissionsScreen('PERMISSIONS', main.env, None) is not None


@fixture
def dominions_roles_screen(main):
    return DominionsRolesScreen('DOMINION ROLES', main.env, MockParent())


@fixture
def permissions_screen(main):
    return PermissionsScreen('PERMISSIONS', main.env, MockParent())


@fixture
def assign_permission_screen(main, permissions_screen):
    permissions_screen.show_assign_permission_screen()
    assign_permission_screen = permissions_screen.env.holder.base_widget
    screen = assign_permission_screen.env.stack.pop()
    assign_permission_screen.env.stack.append(
        DominionsRolesScreen('DOMINIONS ROLE', main.env, MockParent()))
    assign_permission_screen.env.stack.append(screen)
    return assign_permission_screen


def test_dominions_roles_screen_instantiation(dominions_roles_screen):
    assert dominions_roles_screen is not None


def test_dominions_roles_screen_keypress(dominions_roles_screen):
    dominions_roles_screen.keypress(None, 'A')
    focused_widget = dominions_roles_screen.env.holder.original_widget
    assert isinstance(focused_widget, DominionsAddRoleScreen)
    dominions_roles_screen.keypress(None, 'P')
    focused_widget = dominions_roles_screen.env.holder.original_widget
    assert isinstance(focused_widget, PermissionsScreen)
    unhandled = dominions_roles_screen.keypress((40, 40), 'F')
    assert unhandled == 'F'


def test_dominions_add_screen_keypress(main, dominions_add_screen):
    called = False

    class MockMainMenu(Screen):
        def show_dominions_screen(self):
            nonlocal called
            called = True

        def _build_widget(self):
            pass

    dominions_add_screen.env.stack = [MockMainMenu(
        'Mock', main.env), urwid.Text('Mock')]
    dominions_add_screen.name.edit_text = 'Data Server'
    dominions_add_screen.url.edit_text = 'dataserver@nubark.com'

    result = dominions_add_screen.keypress((40, 40), 'ctrl')
    assert result == 'ctrl'

    dominions_add_screen.keypress((40, 40), 'enter')

    assert len(
        dominions_add_screen.management_coordinator
        .dominion_repository.data['knowark']
    ) == 2
    assert called

    result = dominions_add_screen.keypress((40, 40), 'left')
    assert result == 'left'


@fixture
def dominions_add_role_screen(main):
    return DominionsAddRoleScreen('ADD ROLE', main.env, MockParent())


def test_dominions_add_role_screen_keypress(main, dominions_add_role_screen):
    called = False

    class MockRoleScreen(Screen):
        def show_roles_screen(self):
            nonlocal called
            called = True

        def _build_widget(self):
            pass

    dominions_add_role_screen.env.stack = [MockRoleScreen(
        'Mock', main.env), urwid.Text('Mock')]
    dominions_add_role_screen.name.edit_text = 'admin'
    dominions_add_role_screen.description.edit_text = "System's Administrator"

    result = dominions_add_role_screen.keypress((40, 40), 'ctrl')
    assert result == 'ctrl'

    dominions_add_role_screen.keypress((40, 40), 'enter')

    assert len(
        dominions_add_role_screen.management_coordinator
        .role_repository.data['knowark']) == 2
    assert called

    result = dominions_add_role_screen.keypress((40, 40), 'left')
    assert result == 'left'


def test_permissions_screen_show_assign_permission_screen(permissions_screen):
    permissions_screen.show_assign_permission_screen()
    assert isinstance(permissions_screen.env.holder.base_widget,
                      AssignPermissionScreen)


def test_permissions_screen_keypress_a(permissions_screen):
    permissions_screen.dominion["id"] = str(uuid4())
    permissions_screen.keypress((0, 0), "A")
    assert isinstance(permissions_screen.env.holder.base_widget,
                      AssignPermissionScreen)


def test_permissions_screen_keypress_unhandled(permissions_screen):
    assert permissions_screen.keypress((0, 0), "F") == "F"


def test_assign_permission_screen_no_parent(main):
    assert AssignPermissionScreen(
        'ASSIGN PERMISSION', main.env, None) is not None


def test_assign_permission_screen_build_resource_selection(
        assign_permission_screen):
    resource_selection = assign_permission_screen.resource_selection
    assert len(resource_selection.item_list_collector("")) == 1
    assert len(resource_selection.item_formatter(
        {'name': 'Jhon Jairo'})) == len("Jhon Jairo")


def test_assign_permission_screen_build_permission_selection(
        assign_permission_screen):
    permission_selection = assign_permission_screen.permission_selection
    assert len(permission_selection.item_list_collector("")) == 0
    assign_permission_screen.resource_selection.selected = {'id': '1'}
    assert len(permission_selection.item_list_collector("")) == 1
    assert len(permission_selection.item_formatter(
        {'policy': 'My policy'})) == len("My policy")


def test_assign_permission_screen_add_permission(assign_permission_screen):
    assign_permission_screen.role = {'id': '1'}
    assign_permission_screen.permission_selection.selected = {
        'permission_id': '1'}
    assign_permission_screen._add_permission(None)


def test_assign_permission_screen_add_permission_no_permision(
        assign_permission_screen):
    assign_permission_screen._add_permission(None)
    assert isinstance(
        assign_permission_screen.env.holder.base_widget, DominionsRolesScreen)
