import urwid
from authark.infrastructure.terminal.framework.table import Table
from authark.infrastructure.terminal.framework.screen import Screen
from .users_actions import UsersAddScreen, UsersDeleteScreen, UsersUpdateScreen
from .users_credentials import UsersCredentialsScreen
from .users_roles import UsersRolesScreen


class UsersScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_reporter = self.env.context.resolve('AutharkReporter')
        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'success_bg')

        footer = urwid.Text([
            "Press (", ("success", "A"), ") to add a new record. ",
            "Press (", ("light", "C"), ") to show credentials. ",
            "Press (", ("info", "R"), ") to show roles. ",
            "Press (", ("primary", "U"), ") to update a record. ",
            "Press (", ("danger", "D"), ") to delete a record. "
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        box_table = self.build_table(domain=[])
        self.search_user = urwid.Edit()
        urwid.connect_signal(self.search_user, 'change', self.on_search_user)

        self.pile = urwid.Pile([
            urwid.Columns([urwid.Text("SEARCH:", align='center'),
                           self.search_user]),
            urwid.Divider("="),
            box_table
        ])
        body = urwid.Filler(self.pile)

        frame = urwid.Frame(header=header, body=body, footer=footer)
        return frame

    def on_search_user(self, widget, value):
        domain = []
        if value:
            domain = [('username', 'ilike', f"%{value}%")]

        box_table = self.build_table(domain)
        self.pile.contents[-1] = (box_table, self.pile.options('pack', None))

    def build_table(self, domain):
        headers_list = ['username', 'email']
        data = self.auth_reporter.search_users(domain)
        table = Table(data, headers_list)
        return urwid.BoxAdapter(table, 24)

    def show_roles_screen(self):
        screen = UsersRolesScreen("USER'S ROLES", self.env, self)
        return self._open_screen(screen)

    def keypress(self, size, key):
        if self.pile.focus_position == 0:
            return super().keypress(size, key)
        if key in ('a', 'A'):
            screen = UsersAddScreen('ADD USER', self.env, self)
            return self._open_screen(screen)
        if key in ('u', 'U'):
            screen = UsersUpdateScreen('UPDATE USER', self.env, self)
            return self._open_screen(screen)
        if key in ('d', 'D'):
            screen = UsersDeleteScreen('DELETE USER', self.env, self)
            return self._open_screen(screen)
        if key in ('c', 'C'):
            screen = UsersCredentialsScreen(
                "USER'S CREDENTIALS", self.env, self)
            return self._open_screen(screen)
        if key in ('r', 'R', 'enter'):
            self.show_roles_screen()
        return super().keypress(size, key)
