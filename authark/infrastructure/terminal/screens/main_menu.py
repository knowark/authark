import urwid
from typing import Dict, Callable
from ..framework import Screen, Environment
from .users import UsersScreen
from .dominions import DominionsScreen
from .policies import PoliciesScreen
from .tenants import TenantsScreen


class MainMenu(Screen):

    def _build_widget(self) -> urwid.Widget:
        title = urwid.AttrMap(
            urwid.Text('AUTHARK', align='center'), 'secondary_bg')
        tenant_button = urwid.Button(
            'COMFACAUCA', on_press=self.show_tenants_screen)
        tenant_button._label.align = 'center'
        tenant = urwid.AttrMap(
            tenant_button, 'primary_bg')
        header = urwid.Pile([title, tenant])
        widget_list = [
            urwid.Divider(),
            self._build_menu_option('Users', self.show_users_screen),
            self._build_menu_option('Dominions', self.show_dominions_screen),
            self._build_menu_option('Policies', self.show_policies_screen)
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

    def show_tenants_screen(self, button=None):
        screen = TenantsScreen('TENANTS', self.env, self)
        return self._open_screen(screen)

    def show_users_screen(self, button=None):
        screen = UsersScreen('USERS', self.env)
        return self._open_screen(screen)

    def show_dominions_screen(self, button=None):
        screen = DominionsScreen('DOMINIONS', self.env)
        return self._open_screen(screen)

    def show_policies_screen(self, button=None):
        screen = PoliciesScreen('POLICIES', self.env)
        return self._open_screen(screen)
