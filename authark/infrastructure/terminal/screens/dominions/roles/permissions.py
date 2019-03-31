import urwid
from ....framework import Screen, Table, Selection


class PermissionsScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.composing_reporter = self.env.context.resolve(
            'ComposingReporter')
        self.auth_reporter = self.env.context.resolve(
            'AutharkReporter')

        self.dominion = self.parent.dominion
        self.role = self.parent.table.get_selected_item()
        role_id = self.role['id']
        role_name = self.role['name']
        title = "{}: {}".format(self.name, role_name)

        header = urwid.AttrMap(
            urwid.Text(title, align='center'), 'warning_bg')

        footer = urwid.Text([
            "Press (", ("success", "A"), ") to add a new record. ",
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        # Roles
        headers_list = ['resource', 'policy', 'value']
        data = self.composing_reporter.list_role_permissions(role_id)

        self.table = Table(data, headers_list)
        body = self.table

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 60),
            valign='middle', height=('relative', 60),
            min_width=20, min_height=9)

        return widget

    def show_assign_permission_screen(self):
        screen = AssignPermissionScreen('ASSIGN PERMISSION', self.env, self)
        return self._open_screen(screen)

    def keypress(self, size, key):
        if key in ('a', 'A') and self.dominion['id']:
            return self.show_assign_permission_screen()
        return super().keypress(size, key)


class AssignPermissionScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_reporter = self.env.context.resolve(
            'AutharkReporter')
        self.composing_reporter = self.env.context.resolve(
            'ComposingReporter')
        self.assignment_coordinator = self.env.context.resolve(
            'AssignmentCoordinator')

        self.role = self.parent.role
        self.dominion = self.parent.dominion

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'success_bg')

        footer = urwid.Text([
            "Press (", ("success", "Enter"), ") to save. "
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        # self.resource = self.parent.resource
        self.accept_button = urwid.Button('Accept')
        self.accept_button._label.align = 'center'
        urwid.connect_signal(self.accept_button, 'click', self._add_permission)

        self.resource_selection = self._build_resource_selection()
        self.permission_selection = self._build_permission_selection()

        body = urwid.Filler(urwid.Pile([
            self.resource_selection,
            self.permission_selection,
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

    def _build_resource_selection(self):
        def item_list_collector(x):
            resources = self.auth_reporter.search_resources(
                [('dominion_id', '=', self.dominion['id'])])
            return resources

        def item_formatter(item):
            return str(item.get('name', ''))

        return Selection('Resource', item_list_collector, item_formatter)

    def _build_permission_selection(self):
        def item_list_collector(x):
            resource = self.resource_selection.selected
            if not resource:
                return []
            permissions = self.composing_reporter.list_resource_policies(
                resource['id'])
            return permissions

        def item_formatter(item):
            return str(item.get('policy', ''))

        return Selection('Permission', item_list_collector, item_formatter)

    def _add_permission(self, button: urwid.Button):
        permission = self.permission_selection.selected

        if not permission:
            return

        assigned = self.assignment_coordinator.assign_permission(
            self.role.get('id'), permission.get('permission_id'))

        self._go_back()

    def _go_back(self):
        self._back()
        users_screen = self.env.stack.pop()
        users_screen.show_permissions_screen()
