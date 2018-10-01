import urwid
from pytest import fixture, raises
from authark.infrastructure.config.context import Context
from authark.infrastructure.terminal.framework.screen import Screen


def test_screen_instantiation(screen):
    assert screen is not None


def test_screen_build_widget_not_implemented():
    with raises(NotImplementedError):
        screen = Screen('Test', None)


def test_screen_open_screen(screen):
    class SecondMockScreen(Screen):
        def _build_widget(self):
            pass
    second_mock_screen = SecondMockScreen('Second', screen.env)
    screen._open_screen(second_mock_screen)
    assert screen.env.holder.original_widget == second_mock_screen


def test_screen_back(screen):
    stack = [urwid.Text('One'), urwid.Text('Two')]
    screen.env.stack = list(stack)
    screen._back()
    assert screen.env.holder.original_widget == stack[1]


def test_screen_keypress(screen):
    result = screen.keypress(None, 'down')
    assert result == 'down'
    stack = [urwid.Text('One'), urwid.Text('Two')]
    screen.env.stack = list(stack)
    screen.keypress(None, 'esc')
    assert screen.env.holder.original_widget == stack[1]
