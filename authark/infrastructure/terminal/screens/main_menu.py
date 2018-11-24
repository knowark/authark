import urwid
from typing import Dict, Callable
from ..framework import Screen, Environment
from .users import UsersScreen
from .dominions import DominionsScreen


class MainMenu(Screen):

    def _build_widget(self) -> urwid.Widget:
        header = urwid.AttrMap(
            urwid.Text('AUTHARK', align='center'), 'primary_bg')
        widget_list = [
            urwid.Divider(),
            self._build_menu_option('Users', self.show_users_screen),
            self._build_menu_option('Dominions', self.show_dominions_screen)
        ]

        body = urwid.ListBox(urwid.SimpleFocusListWalker(widget_list))

        footer = urwid.Text([
            "Press (", ("warning", "Alt Q"), ") to exit. "
        ])

        frame = urwid.Frame(header=header, body=body, footer=footer)

        return frame

    def _build_menu_option(self, name, callback):
        button = urwid.Button(name)
        urwid.connect_signal(button, 'click', callback)
        return urwid.AttrMap(button, 'info')

    def show_users_screen(self, button=None):
        screen = UsersScreen('USERS', self.env)
        return self._open_screen(screen)

    def show_dominions_screen(self, button=None):
        screen = DominionsScreen('DOMINIONS', self.env)
        return self._open_screen(screen)
