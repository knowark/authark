import urwid
from typing import Dict, Callable
from authark.infrastructure.terminal.framework.screen import Screen
from authark.infrastructure.terminal.framework.environment import Environment
from authark.infrastructure.terminal.screens.users.users import UsersScreen


class MainMenu(Screen):

    def _build_widget(self) -> urwid.Widget:
        header = urwid.AttrMap(
            urwid.Text('AUTHARK', align='center'), 'titlebar')
        widget_list = [
            header,
            urwid.Divider(),
            self._build_menu_option('Users', self.show_users_screen)
        ]

        widget = urwid.ListBox(urwid.SimpleFocusListWalker(widget_list))

        return widget

    def _build_menu_option(self, name, callback):
        button = urwid.Button(name)
        urwid.connect_signal(button, 'click', callback)
        return urwid.AttrMap(button, 'reversed')

    def show_users_screen(self, button=None):
        screen = UsersScreen('USERS', self.env)
        return self._open_screen(screen)
