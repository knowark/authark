import urwid
from pytest import raises, fixture
from authark.infrastructure.terminal.framework import Table, Screen
from authark.infrastructure.terminal.screens.dominions import (
    DominionsScreen, DominionsAddScreen, DominionsRolesScreen,
    DominionsAddRoleScreen)
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


@fixture
def dominions_roles_screen(main):
    return DominionsRolesScreen('DOMINION ROLES', main.env, MockParent())


def test_dominions_roles_screen_instantiation(dominions_roles_screen):
    assert dominions_roles_screen is not None


def test_dominions_roles_screen_keypress(dominions_roles_screen):
    dominions_roles_screen.keypress(None, 'A')
    focused_widget = dominions_roles_screen.env.holder.original_widget
    assert isinstance(focused_widget, DominionsAddRoleScreen)
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
