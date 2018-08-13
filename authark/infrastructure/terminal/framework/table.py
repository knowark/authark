import urwid
from typing import List, Dict, Any


class Table(urwid.WidgetWrap):

    def __init__(self, data_list: List[Dict[str, Any]],
                 headers_list: List[str]) -> None:
        header = self._build_header(headers_list)
        widget_list = [header]
        for row_dict in data_list:
            row_widget = TableRow(row_dict, headers_list)
            widget_list.append(row_widget)

        widget = urwid.ListBox(urwid.SimpleFocusListWalker(widget_list))
        widget.set_focus(0)
        super().__init__(widget)

    def _build_header(self, headers_list: List[str]) -> urwid.Widget:
        headers_widgets = [urwid.Pile([
            urwid.Text(header.upper(), align='center'),
            urwid.Text('-' * len(header), align='center')])
            for header in headers_list]

        return urwid.Columns(headers_widgets)

    def keypress(self, size, key):
        if key == 'home':
            self._w.set_focus(0)
            key = None
        elif key == 'end':
            self._w.set_focus(len(self._w.body) - 1)
            key = None
        elif key == 'up':
            position = max(0, self._w.focus_position - 1)
            self._w.set_focus(position)
            key = None
        elif key == 'down':
            position = min(len(self._w.body) - 1, self._w.focus_position + 1)
            self._w.set_focus(position)
            key = None
        return key


class TableRow(urwid.WidgetWrap):

    def __init__(self, row_dict: Dict[str, Any],
                 headers_list: List[str]) -> None:
        items_list = []
        for key in headers_list:
            widget = urwid.Text(str(row_dict[key]), align='center')
            items_list.append(widget)

        widget = urwid.AttrMap(
            urwid.Columns(items_list), None, focus_map='reversed')

        super().__init__(widget)
