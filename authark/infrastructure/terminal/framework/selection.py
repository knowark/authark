import urwid
from typing import List, Dict, Any, Callable


class Selection(urwid.WidgetWrap):

    def __init__(self,
                 label: str,
                 item_list_collector: Callable,
                 item_formatter: Callable) -> None:

        self.selected = None
        self.item_list_collector = item_list_collector
        self.item_formatter = item_formatter

        self.label = urwid.Text(label.upper(), align='center')
        self.content = urwid.Text('[-----]', align='center')
        self.button = urwid.Button('v')
        self.button._label.align = 'center'

        self.combobox = urwid.Columns([
            ('weight', 4, urwid.LineBox(self.label)),
            ('weight', 5, urwid.LineBox(self.content)),
            ('weight', 1, urwid.LineBox(self.button))
        ])

        self.holder = urwid.WidgetPlaceholder(self.combobox)

        super().__init__(self.holder)

        urwid.connect_signal(self.button, 'click', self._show_selection)

    def _show_selection(self, button: urwid.Button):
        self.items = self.item_list_collector(None)
        data_list = self.item_list_collector(self.items)
        selection_list = self._build_selection_list(data_list)

        self.holder.original_widget = selection_list

    def _build_selection_list(self, data_list):
        return SelectionList(
            data_list, self.item_formatter, self._set_selected)

    def _set_selected(self, item: Any):
        self.selected = item
        value = self.item_formatter(item) if item else '[-----]'

        self.content.set_text(value)
        self.holder.original_widget = self.combobox


class SelectionList(urwid.WidgetWrap):

    def __init__(self, item_list, item_formatter, selection_callback):
        self.item_list = item_list

        widget_list = []
        for item in self.item_list:
            value = item_formatter(item)
            widget = urwid.AttrMap(
                urwid.Text(value), None, focus_map='reversed')
            widget_list.append(widget)

        if not widget_list:
            widget_list = [urwid.AttrMap(
                urwid.Text('[-----]'), None, focus_map='reversed')]

        self.selection_callback = selection_callback
        self.item_formatter = item_formatter
        self.list_box = urwid.ListBox(
            urwid.SimpleFocusListWalker(widget_list))

        widget = urwid.BoxAdapter(self.list_box, 1)

        super().__init__(widget)

    def keypress(self, size, key):
        if key == 'enter':
            selected_item = None
            if self.item_list:
                selected_item = self.item_list[self.list_box.focus_position]
            self.selection_callback(selected_item)

        return super().keypress(size, key)
