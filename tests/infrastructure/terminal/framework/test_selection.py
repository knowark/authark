import urwid
from authark.infrastructure.terminal.framework import Selection


def test_selection_instantiation(selection):
    assert selection is not None
