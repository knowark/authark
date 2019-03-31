import urwid
from ....framework import Screen, Table


class PermissionsScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_reporter = self.env.context.resolve(
            'AutharkReporter')

        self.dominion = self.parent.table.get_selected_item()
        dominion_id = self.dominion['id']
        dominion_name = self.dominion['name']
        title = "{}: {}".format(self.name, dominion_name)

        header = urwid.AttrMap(
            urwid.Text(title, align='center'), 'warning_bg')

        footer = urwid.Text([
            "Press (", ("success", "A"), ") to add a new record. ",
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        # Roles
        headers_list = ['resource', 'policy', 'value']
        data = self.auth_reporter.search_roles(
            [('dominion_id', '=', dominion_id)])
        data = []

        self.table = Table(data, headers_list)
        body = self.table

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 60),
            valign='middle', height=('relative', 60),
            min_width=20, min_height=9)

        return widget

    def show_add_role_screen(self):
        screen = DominionsAddRoleScreen('ADD ROLE', self.env, self)
        return self._open_screen(screen)

    def keypress(self, size, key):
        if key in ('a', 'A') and self.dominion['id']:
            return self.show_add_role_screen()
        return super().keypress(size, key)
