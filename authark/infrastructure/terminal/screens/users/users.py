import urwid
from authark.infrastructure.terminal.framework.table import Table
from authark.infrastructure.terminal.framework.screen import Screen
from authark.infrastructure.terminal.screens.users.users_actions import (
    UsersAddScreen, UsersDeleteScreen)


class UsersScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_reporter = self.env.context.registry['auth_reporter']
        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'heading')

        footer = urwid.Text([
            "Press (", ("add button", "A"), ") to add a new record. ",
            "Press (", ("update button", "U"), ") to update a record. ",
            "Press (", ("remove button", "R"), ") to remove a record. "
            "Press (", ("back button", "Esc"), ") to go back. "
        ])

        headers_list = ['username', 'email']
        data = self.auth_reporter.search_users([])

        self.table = Table(data, headers_list)
        body = self.table

        frame = urwid.Frame(header=header, body=body, footer=footer)

        return frame

    def keypress(self, size, key):
        if key in ('a', 'A'):
            screen = UsersAddScreen('ADD USER', self.env, self)
            return self._open_screen(screen)
        if key in ('d', 'D'):
            screen = UsersDeleteScreen('DELETE USER', self.env, self)
            return self._open_screen(screen)
        return super().keypress(size, key)
