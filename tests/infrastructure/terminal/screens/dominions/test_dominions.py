import urwid
from pytest import raises, fixture
from authark.infrastructure.terminal.screens.dominions import (
    DominionsScreen, DominionsAddScreen)


@fixture
def dominions_screen(main):
    return DominionsScreen('DOMINIONS', main.env)


def test_dominions_screen_instantiation(dominions_screen):
    assert dominions_screen is not None


def test_dominions_screen_keypress(dominions_screen):
    dominions_screen.table.keypress(None, 'down')
    dominions_screen.keypress(None, 'A')
    focused_widget = dominions_screen.env.holder.original_widget
    assert isinstance(focused_widget, DominionsAddScreen)
    # dominions_screen.keypress(None, 'D')
    # focused_widget = dominions_screen.env.holder.original_widget
    # assert isinstance(focused_widget, DominionsDeleteScreen)
    # dominions_screen.keypress(None, 'C')
    # focused_widget = dominions_screen.env.holder.original_widget
    # assert isinstance(focused_widget, DominionsCredentialsScreen)
    unhandled = dominions_screen.keypress((40, 40), 'F')
    assert unhandled == 'F'
