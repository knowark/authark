import urwid
from authark.infrastructure.terminal.framework.screen import Screen


class UsersAddScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_coordinator = self.env.context.registry['auth_coordinator']

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'titlebar')

        footer = urwid.Text([
            "Press (", ("add button", "Enter"), ") to save. "
            "Press (", ("back button", "Esc"), ") to go back. "
        ])

        self.username = urwid.Edit()
        self.email = urwid.Edit()
        self.password = urwid.Edit()

        body = urwid.Pile([
            urwid.Columns([
                urwid.Text("Username: ", align='center'), self.username]),
            urwid.Columns([
                urwid.Text("Email: ", align='center'), self.email]),
            urwid.Columns([
                urwid.Text("Password: ", align='center'), self.password]),
        ])
        body = urwid.Padding(urwid.Filler(body), align='center', width=80)

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 50),
            valign='middle', height=('relative', 50),
            min_width=20, min_height=9)

        return widget

    def keypress(self, size, key):
        if key == 'enter':
            username = self.username.edit_text
            email = self.email.edit_text
            password = self.password.edit_text
            user = self.auth_coordinator.register(username, email, password)
            self.logger.debug("User -->> %s", user)
            self._go_back()
        return super().keypress(size, key)

    def _go_back(self):
        self._back()
        main_menu = self.env.stack.pop()
        main_menu.show_users_screen()


class UsersDeleteScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_coordinator = self.env.context.registry['auth_coordinator']

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'titlebar')

        footer = urwid.Text([
            "Press (", ("remove button", "Enter"), ") to delete. "
            "Press (", ("back button", "Esc"), ") to go back. "
        ])

        table = self.parent.table
        self.selected_item = table.get_selected_item()
        body = urwid.Pile([
            urwid.Text("Are you sure you want to delete the following user?"),
            urwid.Divider(),
            urwid.Text(
                "Username: {username}".format(**self.selected_item)),
            urwid.Text(
                "ID: {id}".format(**self.selected_item)),
        ])
        body = urwid.Padding(urwid.Filler(body), align='center', width=80)

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 50),
            valign='middle', height=('relative', 50),
            min_width=20, min_height=9)

        return widget

    def keypress(self, size, key):
        if key == 'enter':
            id = self.selected_item.get('id')
            user = self.auth_coordinator.deregister(id)
            self.logger.debug("User: %s has been unregistered!", user)
            self._go_back()
        return super().keypress(size, key)

    def _go_back(self):
        self._back()
        main_menu = self.env.stack.pop()
        main_menu.show_users_screen()
