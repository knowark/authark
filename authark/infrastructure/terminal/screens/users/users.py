import urwid
from authark.infrastructure.terminal.framework.table import Table
from authark.infrastructure.terminal.framework.screen import Screen
from authark.infrastructure.terminal.screens.users.users_actions import (
    UsersAddScreen)


class UsersScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'heading')

        footer = urwid.Text([
            "Press (", ("add button", "A"), ") to add a new record. ",
            "Press (", ("update button", "U"), ") to update a record. ",
            "Press (", ("remove button", "R"), ") to remove a record. "
            "Press (", ("back button", "Esc"), ") to go back. "
        ])

        # Create the contents table
        data = [
            {'name': "Esteban", 'surname': "Echeverry", 'age': 29},
            {'name': "Gabriel", 'surname': "Echeverry", 'age': 26},
            {'name': "Valentina", 'surname': "Echeverry", 'age': 34}
        ]
        data = data * 5
        self.table = Table(data)
        body = self.table

        frame = urwid.Frame(header=header, body=body, footer=footer)

        return frame

    def keypress(self, size, key):
        if key in ('a', 'A'):
            screen = UsersAddScreen('ADD USER', self.env, self)
            return self._open_screen(screen)
        return super().keypress(size, key)