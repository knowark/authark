import urwid
from ...framework import Screen, Table


class UsersCredentialsScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_coordinator = self.env.context.registry['AuthCoordinator']
        self.auth_reporter = self.env.context.registry['AutharkReporter']

        if not self.parent:
            return

        self.selected_item = self.parent.table.get_selected_item()
        username = self.selected_item.get('username')
        title = "{}: {}".format(self.name, username)

        header = urwid.AttrMap(
            urwid.Text(title, align='center'), 'primary_bg')

        footer = urwid.Text([
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        # Credentials
        headers_list = ['id', 'type', 'client', 'value']
        data = self.auth_reporter.search_credentials(
            [('user_id', '=', self.selected_item.get('id'))])

        body = Table(data, headers_list)

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 70),
            valign='middle', height=('relative', 70),
            min_width=20, min_height=9)

        return widget
