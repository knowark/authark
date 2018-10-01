import urwid
from pytest import fixture
from authark.infrastructure.config.context import Context
from authark.infrastructure.terminal.framework.screen import Screen


def test_screen_instantiation(screen):
    assert screen is not None
