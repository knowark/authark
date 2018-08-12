import urwid
from typing import Dict, Callable
from authark.infrastructure.terminal.framework.screen import Screen
from authark.infrastructure.terminal.framework.environment import Environment
from authark.infrastructure.terminal.screens.users import UsersScreen


class MainMenu(Screen):

    def _build_widget(self) -> urwid.Widget:
        header = urwid.AttrMap(
            urwid.Text('AUTHARK', align='center'), 'titlebar')
        widget_list = [
            header,
            urwid.Divider(),
            self._build_menu_option('Users', self._show_users_screen)
        ]

        widget = urwid.ListBox(urwid.SimpleFocusListWalker(widget_list))

        return widget

    def _build_menu_option(self, name, callback):
        self.logger.debug('Build Menu: %s', name)
        button = urwid.Button(name)
        urwid.connect_signal(button, 'click', callback)
        return urwid.AttrMap(button, 'reversed')

    def _show_users_screen(self, button):
        screen = UsersScreen('USERS', self.env)
        self.logger.debug('SCREEN: %s', screen)
        return self._open_screen(screen)
