import urwid
from ...framework import Screen, Table


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
            align='center', width=('relative', 70),
            valign='middle', height=('relative', 70),
            min_width=20, min_height=9)

        return widget

    def show_add_resource_screen(self):
        screen = DominionsAddResourceScreen('ADD RESOURCE', self.env, self)
        return self._open_screen(screen)

    def keypress(self, size, key):
        if key in ('a', 'A') and self.dominion['id']:
            return self.show_add_resource_screen()
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
