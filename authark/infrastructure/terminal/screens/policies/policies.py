import urwid
from ...framework import Table, Screen
from .policies_actions import (
    PoliciesAddScreen)


class PoliciesScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_reporter = self.env.context.resolve(
            'AutharkReporter')
        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'secondary_bg')

        footer = urwid.Text([
            "Press (", ("success", "A"), ") to add a new record. ",
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        headers_list = ['name', 'type', 'value']
        data = self.auth_reporter.search_policies([])

        self.table = Table(data, headers_list)
        body = self.table

        frame = urwid.Frame(header=header, body=body, footer=footer)

        return frame

    def keypress(self, size, key):
        if key in ('a', 'A'):
            screen = PoliciesAddScreen('ADD POLICY', self.env, self)
            return self._open_screen(screen)
        return super().keypress(size, key)
