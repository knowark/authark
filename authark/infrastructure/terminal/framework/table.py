import urwid
from typing import List, Dict, Any


class Table(urwid.WidgetWrap):

    def __init__(self, data_list: List[Dict[str, Any]]) -> None:
        header = self._build_header(data_list[0])
        widget_list = [header]
        for row_dict in data_list:
            row_widget = TableRow(row_dict)
            widget_list.append(row_widget)

        widget = urwid.ListBox(urwid.SimpleFocusListWalker(widget_list))
        widget.set_focus(1)
        super().__init__(widget)

    def _build_header(self, header_dict: Dict[str, Any]) -> urwid.Widget:
        headers_list = [urwid.Pile([
            urwid.Text(key.upper(), align='center'),
            urwid.Text('-' * len(key), align='center')])
            for key in header_dict.keys()]

        return urwid.Columns(headers_list)

    def keypress(self, size, key):
        # print("superr")

        # text = urwid.Text("YUPIII")
        # frame = urwid.Frame(text)
        # overlay = urwid.Overlay(
        #     frame, self,
        #     align='center', width=('relative', 80),
        #     valign='middle', height=('relative', 80),
        # )

        # return overlay

        if key == 'home':
            self._w.set_focus(1)
            key = None
        elif key == 'end':
            self._w.set_focus(len(self._w.body) - 1)
            key = None
        elif key == 'up':
            position = max(1, self._w.focus_position - 1)
            self._w.set_focus(position)
            key = None
        elif key == 'down':
            position = min(len(self._w.body) - 1, self._w.focus_position + 1)
            self._w.set_focus(position)
            key = None
        return key


class TableRow(urwid.WidgetWrap):

    def __init__(self, row_dict: Dict[str, Any]) -> None:
        items_list = []
        for key, value in row_dict.items():
            widget = urwid.Text(str(value), align='center')
            items_list.append(widget)

        widget = urwid.AttrMap(
            urwid.Columns(items_list), None, focus_map='reversed')

        super().__init__(widget)

    def keypress(self, size, key):
        text = urwid.Text("YUPIII")
        frame = urwid.Frame(text)
        overlay = urwid.Overlay(frame, self)

        return popup.create_pop_up()

        # print("SUPERRRR!!!!  <<<<")
