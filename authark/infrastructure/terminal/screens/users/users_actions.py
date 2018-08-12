import urwid
from authark.infrastructure.terminal.framework.screen import Screen


class UsersAddScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_coordinator = self.env.context.registry['auth_coordinator']

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'titlebar')

        footer = urwid.Text([
            "Press (", ("back button", "B"), ") to go back. "
        ])

        body = urwid.Pile([
            urwid.Columns([
                urwid.Text("Username: ", align='center'), urwid.Edit()]),
            urwid.Columns([
                urwid.Text("Email: ", align='center'), urwid.Edit()]),
            urwid.Columns([
                urwid.Text("Password: ", align='center'), urwid.Edit()]),
        ])
        body = urwid.Padding(urwid.Filler(body), align='center', width=80)

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 50),
            valign='middle', height=('relative', 50),
            min_width=20, min_height=9)

        return widget
