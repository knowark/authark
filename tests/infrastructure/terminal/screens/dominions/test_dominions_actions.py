import urwid
from pytest import raises, fixture
from authark.infrastructure.terminal.framework.screen import Screen
from authark.infrastructure.terminal.framework.table import Table
from authark.infrastructure.terminal.screens.dominions import (
    DominionsScreen, DominionsAddScreen)


@fixture
def dominions_add_screen(main):
    return DominionsAddScreen('DOMINIONS ADD', main.env)


def test_dominions_add_screen_instantiation(dominions_add_screen):
    assert dominions_add_screen is not None


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
        dominions_add_screen.management_coordinator.dominion_repository.items
    ) == 1
    assert called

    result = dominions_add_screen.keypress((40, 40), 'left')
    assert result == 'left'
