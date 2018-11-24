import urwid
from ...framework import Table, Screen
from .dominions_actions import (
    DominionsAddScreen, DominionsRolesScreen)


class DominionsScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_reporter = self.env.context.registry['auth_reporter']
        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'secondary_bg')

        footer = urwid.Text([
            "Press (", ("success", "A"), ") to add a new record. ",
            "Press (", ("light", "S"), ") to show roles. ",
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        headers_list = ['name', 'url']
        data = self.auth_reporter.search_dominions([])

        self.table = Table(data, headers_list)
        body = self.table

        frame = urwid.Frame(header=header, body=body, footer=footer)

        return frame

    def show_roles_screen(self):
        screen = DominionsRolesScreen('DOMINION ROLES', self.env, self)
        return self._open_screen(screen)

    def keypress(self, size, key):
        if key in ('a', 'A'):
            screen = DominionsAddScreen('ADD DOMINION', self.env, self)
            return self._open_screen(screen)
        if key in ('s', 'S', 'enter') and len(self.table):
            return self.show_roles_screen()
        return super().keypress(size, key)
