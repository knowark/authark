import urwid
from ...framework import Screen, Table, Selection


class UsersRolesScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.management_coordinator = self.env.context.registry[
            'management_coordinator']
        self.auth_reporter = self.env.context.registry['auth_reporter']
        self.composing_reporter = self.env.context.registry[
            'composing_reporter']

        if not self.parent:
            return

        self.selected_item = self.parent.table.get_selected_item()
        user_id = self.selected_item.get('id')
        username = self.selected_item.get('username')
        title = "{}: {}".format(self.name, username)

        header = urwid.AttrMap(
            urwid.Text(title, align='center'), 'warning_bg')

        footer = urwid.Text([
            "Press (", ("success", "A"), ") to assign a role. "
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        # Roles
        headers_list = ['role', 'dominion']
        data = self.composing_reporter.list_user_roles(user_id)

        body = Table(data, headers_list)

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 70),
            valign='middle', height=('relative', 70),
            min_width=20, min_height=9)

        return widget

    def show_assign_role_screen(self):
        screen = UsersAssignRoleScreen('ASSIGN ROLE', self.env, self)
        return self._open_screen(screen)

    def keypress(self, size, key):
        if key in ('a', 'A'):
            return self.show_assign_role_screen()
        return super().keypress(size, key)


class UsersAssignRoleScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_reporter = self.env.context.registry['auth_reporter']

        self.management_coordinator = self.env.context.registry[
            'management_coordinator']

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'success_bg')

        footer = urwid.Text([
            "Press (", ("success", "Enter"), ") to save. "
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        self.accept_button = urwid.Button('Accept')
        self.accept_button._label.align = 'center'
        urwid.connect_signal(self.accept_button, 'click', self._add_ranking)

        self.dominion_selection = self._build_dominion_selection()
        self.role_selection = self._build_role_selection()

        body = urwid.Filler(urwid.Pile([
            urwid.Text('Assign Role...', align='center'),
            self.dominion_selection,
            self.role_selection,
            urwid.Divider(' ', 1, 1),
            urwid.AttrMap(self.accept_button, 'success')
        ]))

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 60),
            valign='middle', height=('relative', 60),
            min_width=20, min_height=9)

        return widget

    def _build_dominion_selection(self):
        def item_list_collector(x): return ['X', 'Y', 'Z']

        def item_formatter(x): return str(x)

        return Selection('Dominion', item_list_collector, item_formatter)

    def _build_role_selection(self):
        def item_list_collector(x):
            if not self.dominion_selection.selected:
                return []
            return ['A', 'B', 'C', 'D', 'E']

        def item_formatter(x): return str(x)

        return Selection('Role', item_list_collector, item_formatter)

    def keypress(self, size, key):
        return super().keypress(size, key)

    def _add_ranking(self, button: urwid.Button):
        pass
