import urwid
from authark.infrastructure.terminal.framework.screen import Screen


class UsersAddScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'titlebar')

        footer = urwid.Text([
            "Press (", ("back button", "B"), ") to go back. "
        ])

        body = urwid.Filler(urwid.Text("Add Users"))
        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = frame

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
            min_width=20, min_height=9)

        return widget
