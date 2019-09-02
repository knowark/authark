import urwid
from typing import Set
from authark.infrastructure.terminal.framework import Table, Screen
from .tenants_actions import TenantsDetailsScreen
# from .tenants_actions import TenantsExportScreen


class TenantsScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.tenancy_supplier = self.env.context.resolve('TenantSupplier')
        self.session_coordinator = self.env.context.resolve(
            'SessionCoordinator')

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'success_bg')

        footer = urwid.Text([
            "Press (", ("success", "A"), ") to add a new record. ",
            "Press (", ("info", "D"), ") to show tenant's details. ",
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        if not self.parent:
            return

        self.selected_tenants: Set[str] = set()

        self.table = self.build_table(domain=[])
        select_button = urwid.Button('SELECT ALL')
        select_button._label.align = 'center'
        # export_button = urwid.Button('EXPORT', self.show_export_screen)
        # export_button._label.align = 'center'

        commands = urwid.Columns([
            urwid.AttrMap(select_button, 'success'),
            # urwid.AttrMap(export_button, 'warning')
        ])
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
        tenants = self.tenancy_supplier.search_tenants(domain)
        data = []
        for item in tenants:
            check = urwid.CheckBox('', True, False,
                                   self.toggle_tenant, item['id'])
            data.append({**{'': check}, **item})
            self.selected_tenants.add(item['id'])

        return Table(data, headers_list)

    def toggle_tenant(self, check_box, state, tenant_id):
        if tenant_id in self.selected_tenants:
            self.selected_tenants.remove(tenant_id)
        else:
            self.selected_tenants.add(tenant_id)

    def set_current_tenant(self):
        self.selected_item = self.table.get_selected_item()
        self.session_coordinator.set_tenant(self.selected_item)

        self._back()
        main_menu = self.env.holder.original_widget
        main_menu.rebuild()

    def show_details_screen(self):
        screen = TenantsDetailsScreen("TENANT'S DETAILS", self.env, self)
        return self._open_screen(screen)

    # def show_export_screen(self, button=None):
    #     if not self.selected_tenants:
    #         return None
    #     screen = TenantsExportScreen("EXPORT TENANTS", self.env, self)
    #     return self._open_screen(screen)

    def keypress(self, size, key):
        if self.pile.focus_position <= 1:
            return super().keypress(size, key)
        if key in ('enter'):
            self.set_current_tenant()
        if key in ('d', 'D'):
            self.show_details_screen()
        return super().keypress(size, key)
