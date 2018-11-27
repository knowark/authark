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
            "Press (", ("danger", "D"), ") to deassign a role. "
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        # Roles
        headers_list = ['role', 'dominion']
        data = self.composing_reporter.list_user_roles(user_id)

        self.table = Table(data, headers_list)
        body = self.table

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

    def show_deassign_role_screen(self):
        screen = UsersDeassignRoleScreen('DEASSIGN ROLE', self.env, self)
        return self._open_screen(screen)

    def keypress(self, size, key):
        if key in ('a', 'A'):
            return self.show_assign_role_screen()
        if key in ('d', 'D'):
            return self.show_deassign_role_screen()
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

        self.user = self.parent.selected_item
        self.accept_button = urwid.Button('Accept')
        self.accept_button._label.align = 'center'
        urwid.connect_signal(self.accept_button, 'click', self._add_ranking)

        self.dominion_selection = self._build_dominion_selection()
        self.role_selection = self._build_role_selection()

        body = urwid.Filler(urwid.Pile([
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
        def item_list_collector(x):
            dominions = self.auth_reporter.search_dominions([])
            return dominions

        def item_formatter(item):
            return str(item.get('name', ''))

        return Selection('Dominion', item_list_collector, item_formatter)

    def _build_role_selection(self):
        def item_list_collector(x):
            dominion = self.dominion_selection.selected
            if not dominion:
                return []
            roles = self.auth_reporter.search_roles(
                [('dominion_id', '=', dominion.get('id'))])
            return roles

        def item_formatter(item):
            return str(item.get('name', ''))

        return Selection('Role', item_list_collector, item_formatter)

    def _add_ranking(self, button: urwid.Button):
        role = self.role_selection.selected
        if not role:
            return

        assigned = self.management_coordinator.assign_role(
            self.user.get('id'), role.get('id'))

        self._go_back()

    def _go_back(self):
        self._back()
        users_screen = self.env.stack.pop()
        users_screen.show_roles_screen()


class UsersDeassignRoleScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.management_coordinator = self.env.context.registry[
            'management_coordinator']

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
            urwid.Text("Are you sure you want to deassign this role?"),
            urwid.Divider(),
            urwid.Text("DOMINION: {dominion}".format(**self.selected_item)),
            urwid.Text("ROLE: {role}".format(**self.selected_item))
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
            id = self.selected_item.get('ranking_id')
            user = self.management_coordinator.deassign_role(id)
            self._go_back()
        return super().keypress(size, key)

    def _go_back(self):
        self._back()
        users_screen = self.env.stack.pop()
        users_screen.show_roles_screen()
