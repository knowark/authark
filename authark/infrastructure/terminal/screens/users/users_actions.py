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
            self._back()
        return super().keypress(size, key)
