import urwid
from ...framework import Screen, Table


class DominionsAddScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.management_coordinator = self.env.context.registry[
            'management_coordinator']

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'titlebar')

        footer = urwid.Text([
            "Press (", ("add button", "Enter"), ") to save. "
            "Press (", ("back button", "Esc"), ") to go back. "
        ])

        self.name = urwid.Edit()
        self.url = urwid.Edit()

        body = urwid.Pile([
            urwid.Columns([
                urwid.Text("Name: ", align='center'), self.name]),
            urwid.Columns([
                urwid.Text("URL: ", align='center'), self.url])
        ])
        body = urwid.Padding(urwid.Filler(body), align='center', width=80)

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 50),
            valign='middle', height=('relative', 50),
            min_width=20, min_height=9)

        return widget

    def keypress(self, size, key):
        if key == 'enter':
            dominion_dict = {}
            dominion_dict['name'] = self.name.edit_text
            dominion_dict['url'] = self.url.edit_text
            dominion = self.management_coordinator.create_dominion(
                dominion_dict)
            self._go_back()
        if key == 'left':
            return super(urwid.WidgetWrap, self).keypress(size, key)
        return super().keypress(size, key)

    def _go_back(self):
        self._back()
        main_menu = self.env.stack.pop()
        main_menu.show_dominions_screen()
