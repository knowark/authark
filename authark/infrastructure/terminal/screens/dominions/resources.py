import urwid
from ...framework import Screen, Table, Selection


class DominionsResourcesScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_reporter = self.env.context.resolve(
            'AutharkReporter')

        self.dominion = self.parent.table.get_selected_item()
        dominion_id = self.dominion['id']
        dominion_name = self.dominion['name']
        title = "{}: {}".format(self.name, dominion_name)

        header = urwid.AttrMap(
            urwid.Text(title, align='center'), 'info_bg')

        footer = urwid.Text([
            "Press (", ("success", "A"), ") to add a new record. ",
            "Press (", ("info", "P"), ") to show policies. ",
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        # Resources
        headers_list = ['name']
        data = self.auth_reporter.search_resources(
            [('dominion_id', '=', dominion_id)])

        self.table = Table(data, headers_list)
        body = self.table

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
            min_width=20, min_height=9)

        return widget

    def show_add_resource_screen(self):
        screen = DominionsAddResourceScreen('ADD RESOURCE', self.env, self)
        return self._open_screen(screen)

    def show_policies_screen(self):
        screen = ResourcesPoliciesScreen('RESOURCE POLICIES', self.env, self)
        return self._open_screen(screen)

    def keypress(self, size, key):
        if key in ('a', 'A') and self.dominion['id']:
            return self.show_add_resource_screen()
        if key in ('p', 'P', 'enter') and len(self.table):
            return self.show_policies_screen()
        return super().keypress(size, key)


class DominionsAddResourceScreen(Screen):

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

        body = urwid.Pile([
            urwid.Columns([
                urwid.Text("Name: ", align='center'), self.name])
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
            resource_dict = {}
            resource_dict['name'] = self.name.edit_text
            resource_dict['dominion_id'] = self.parent.dominion['id']
            resource = self.management_coordinator.create_resource(
                resource_dict)
            self._go_back()
        if key == 'left':
            return super(urwid.WidgetWrap, self).keypress(size, key)
        return super().keypress(size, key)

    def _go_back(self):
        self._back()
        dominion_screen = self.env.stack.pop()
        dominion_screen.show_resources_screen()


class ResourcesPoliciesScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.composing_reporter = self.env.context.resolve(
            'ComposingReporter')

        self.resource = self.parent.table.get_selected_item()
        resource_id = self.resource['id']
        resource_name = self.resource['name']
        title = "{}: {}".format(self.name, resource_name)

        header = urwid.AttrMap(
            urwid.Text(title, align='center'), 'primary_bg')

        footer = urwid.Text([
            "Press (", ("success", "A"), ") to add a new record. ",
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        # Roles
        headers_list = ['policy', 'type', 'value']
        data = self.composing_reporter.list_resource_policies(resource_id)

        self.table = Table(data, headers_list)
        body = self.table

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 70),
            valign='middle', height=('relative', 70),
            min_width=20, min_height=9)

        return widget

    def show_add_policy_screen(self):
        screen = ResourcesAssignPolicyScreen('ASSIGN POLICY', self.env, self)
        return self._open_screen(screen)

    def keypress(self, size, key):
        if key in ('a', 'A') and self.resource['id']:
            return self.show_add_policy_screen()
        return super().keypress(size, key)


class ResourcesAssignPolicyScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_reporter = self.env.context.resolve(
            'AutharkReporter')
        self.assignment_coordinator = self.env.context.resolve(
            'AssignmentCoordinator')

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'success_bg')

        footer = urwid.Text([
            "Press (", ("success", "Enter"), ") to save. "
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        self.resource = self.parent.resource
        self.accept_button = urwid.Button('Accept')
        self.accept_button._label.align = 'center'
        urwid.connect_signal(self.accept_button, 'click', self._add_permission)

        self.policy_selection = self._build_policy_selection()

        body = urwid.Filler(urwid.Pile([
            self.policy_selection,
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

    def _build_policy_selection(self):
        def item_list_collector(x):
            policies = self.auth_reporter.search_policies([])
            return policies

        def item_formatter(item):
            return str(item.get('name', ''))

        return Selection('Policy', item_list_collector, item_formatter)

    def _add_permission(self, button: urwid.Button):
        policy = self.policy_selection.selected

        if not policy:
            return

        assigned = self.assignment_coordinator.assign_policy(
            policy.get('id'), self.resource.get('id'))

        self._go_back()

    def _go_back(self):
        self._back()
        users_screen = self.env.stack.pop()
        users_screen.show_policies_screen()
