import urwid
from authark.infrastructure.terminal.framework.selection import (
    Selection, SelectionList)


def test_selection_instantiation(selection):
    assert selection is not None


def test_selection_show_selection(selection):
    selection._show_selection(urwid.Button("Mock button"))
    assert selection.holder.original_widget.item_list == ['A', 'B', 'C']


def test_selection_set_selected(selection):
    selection._set_selected('B')
    assert selection.content.text == 'B'


def test_selection_key_press():
    item_list = ["A", "B", "C"]

    def mock_callback_function(x: str):
        assert x == "A"

    def mock_item_formater(x: str):
        nonlocal item_list
        assert x in item_list

    selection_list = SelectionList(
        [], mock_item_formater, mock_callback_function)

    selection_list.item_list = item_list
    selection_list.list_box.focus_position = 0
    selection_list.keypress((0,), "enter")
