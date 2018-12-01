import urwid
import json
from ...framework import Screen, Table


class UsersAddScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_coordinator = self.env.context.registry['AuthCoordinator']

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'success_bg')

        footer = urwid.Text([
            "Press (", ("success", "Enter"), ") to save. ",
            "Press (", ("warning", "Esc"), ") to go back. "
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
            self._go_back()
        if key == 'left':
            return super(urwid.WidgetWrap, self).keypress(size, key)
        return super().keypress(size, key)

    def _go_back(self):
        self._back()
        main_menu = self.env.stack.pop()
        main_menu.show_users_screen()


class UsersDeleteScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_coordinator = self.env.context.registry['AuthCoordinator']

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'danger_bg')

        footer = urwid.Text([
            "Press (", ("danger", "Enter"), ") to delete. "
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        if not self.parent:
            return

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
            self._go_back()
        return super().keypress(size, key)

    def _go_back(self):
        self._back()
        main_menu = self.env.stack.pop()
        main_menu.show_users_screen()


class UsersUpdateScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_coordinator = self.env.context.registry['AuthCoordinator']
        self.authark_reporter = self.env.context.registry['AutharkReporter']

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'primary_bg')

        footer = urwid.Text([
            "Press (", ("success", "Enter"), ") to save. ",
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        if not self.parent:
            return

        self.selected_item = self.parent.table.get_selected_item()
        username = self.selected_item.get('username')
        email = self.selected_item.get('email')
        attributes = json.dumps(
            self.selected_item.get('attributes', {}),
            sort_keys=True, indent=4)

        title = "{}: {}".format(self.name, username)

        self.username = urwid.Edit("> ", username)
        self.email = urwid.Edit("> ", email)
        self.attributes = urwid.Edit("", attributes, multiline=True)

        body = urwid.Pile([
            urwid.Columns([
                urwid.Text("Username: ", align='center'), self.username]),
            urwid.Columns([
                urwid.Text("Email: ", align='center'), self.email]),
            urwid.Columns([
                urwid.Text("Attributes: ", align='center'), self.attributes])
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
        if key == 'meta enter':
            print('UPDATE')

            self.selected_item['username'] = self.username.edit_text
            self.selected_item['email'] = self.email.edit_text
            self.selected_item['attributes'] = json.loads(
                self.attributes.edit_text)

            self.auth_coordinator.update(self.selected_item)
            self._go_back()

        if key == 'left':
            return super(urwid.WidgetWrap, self).keypress(size, key)
        return super().keypress(size, key)

    def _go_back(self):
        self._back()
        main_menu = self.env.stack.pop()
        main_menu.show_users_screen()
