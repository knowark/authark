import urwid
from ....framework import Screen, Table
from .permissions import PermissionsScreen


class DominionsRolesScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_reporter = self.env.context.resolve(
            'AutharkReporter')

        self.dominion = self.parent.table.get_selected_item()
        dominion_id = self.dominion['id']
        dominion_name = self.dominion['name']
        title = "{}: {}".format(self.name, dominion_name)

        header = urwid.AttrMap(
            urwid.Text(title, align='center'), 'primary_bg')

        footer = urwid.Text([
            "Press (", ("success", "A"), ") to add a new record. ",
            "Press (", ("info", "P"), ") to show role permissions. ",
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        # Roles
        headers_list = ['name', 'description']
        data = self.auth_reporter.search_roles(
            [('dominion_id', '=', dominion_id)])

        self.table = Table(data, headers_list)
        body = self.table

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 70),
            valign='middle', height=('relative', 70),
            min_width=20, min_height=9)

        return widget

    def show_add_role_screen(self):
        screen = DominionsAddRoleScreen('ADD ROLE', self.env, self)
        return self._open_screen(screen)

    def show_permissions_screen(self):
        screen = PermissionsScreen('ROLE PERMISSIONS', self.env, self)
        return self._open_screen(screen)

    def keypress(self, size, key):
        if key in ('a', 'A') and self.dominion['id']:
            return self.show_add_role_screen()
        if key in ('p', 'P', 'enter') and self.dominion['id']:
            return self.show_permissions_screen()
        return super().keypress(size, key)


class DominionsAddRoleScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.management_coordinator = self.env.context.resolve(
            'ManagementCoordinator')

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'success_bg')

        footer = urwid.Text([
            "Press (", ("success", "Enter"), ") to save. "
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        self.name = urwid.Edit()
        self.description = urwid.Edit()

        body = urwid.Pile([
            urwid.Columns([
                urwid.Text("Name: ", align='center'), self.name]),
            urwid.Columns([
                urwid.Text("Description: ", align='center'), self.description])
        ])
        body = urwid.Padding(urwid.Filler(body), align='center', width=80)

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 60),
            valign='middle', height=('relative', 60),
            min_width=20, min_height=9)

        return widget

    def keypress(self, size, key):
        if key == 'enter':
            role_dict = {}
            role_dict['name'] = self.name.edit_text
            role_dict['dominion_id'] = self.parent.dominion['id']
            role_dict['description'] = self.description.edit_text
            role = self.management_coordinator.create_role(role_dict)
            self._go_back()
        if key == 'left':
            return super(urwid.WidgetWrap, self).keypress(size, key)
        return super().keypress(size, key)

    def _go_back(self):
        self._back()
        dominion_screen = self.env.stack.pop()
        dominion_screen.show_roles_screen()
