import urwid
from authark.infrastructure.terminal.framework import Table, Screen
from .tenants_actions import TenantsDetailsScreen


class TenantsScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.tenancy_reporter = self.env.context.resolve('TenancyReporter')
        self.affiliation_coordinator = self.env.context.resolve(
            'AffiliationCoordinator')

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'success_bg')

        footer = urwid.Text([
            "Press (", ("success", "A"), ") to add a new record. ",
            "Press (", ("info", "D"), ") to show tenant's details. ",
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        if not self.parent:
            return

        self.table = self.build_table(domain=[])
        select_button = urwid.Button('SELECT ALL')
        select_button._label.align = 'center'
        export_button = urwid.Button('EXPORT')
        export_button._label.align = 'center'

        commands = urwid.Columns([
            select_button, export_button])
        box_table = urwid.BoxAdapter(self.table, 24)

        self.pile = urwid.Pile([
            urwid.Divider(),
            commands,
            urwid.Divider(),
            box_table
        ])
        body = urwid.Filler(self.pile)

        frame = urwid.Frame(header=header, body=body, footer=footer)
        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 85),
            valign='middle', height=('relative', 85),
            min_width=20, min_height=9)

        return widget

    def build_table(self, domain):
        headers_list = ['', 'id', 'name', 'slug']
        data = self.tenancy_reporter.search_tenants(domain)
        data = [{**{'': urwid.CheckBox('', True)}, **item}
                for item in data]
        return Table(data, headers_list)

    def set_current_tenant(self):
        self.selected_item = self.table.get_selected_item()
        self.affiliation_coordinator.establish_tenant(self.selected_item['id'])

        self._back()
        main_menu = self.env.holder.original_widget
        main_menu.rebuild()

    def show_details_screen(self):
        screen = TenantsDetailsScreen("TENANT'S DETAILS", self.env, self)
        return self._open_screen(screen)

    def keypress(self, size, key):
        if key in ('enter'):
            self.set_current_tenant()
        if key in ('d', 'D'):
            self.show_details_screen()
        return super().keypress(size, key)
