import urwid
from authark.infrastructure.terminal.framework import Table, Screen


class TenantsScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.tenancy_reporter = self.env.context.resolve('TenancyReporter')
        self.affiliation_coordinator = self.env.context.resolve(
            'AffiliationCoordinator')

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'success_bg')

        footer = urwid.Text([
            "Press (", ("success", "A"), ") to add a new record. ",
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        if not self.parent:
            return

        self.table = self.build_table(domain=[])
        box_table = urwid.BoxAdapter(self.table, 24)

        self.pile = urwid.Pile([
            box_table
        ])
        body = urwid.Filler(self.pile)

        frame = urwid.Frame(header=header, body=body, footer=footer)
        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
            min_width=20, min_height=9)

        return widget

    def on_search_user(self, widget, value):
        domain = []
        if value:
            domain = [('username', 'ilike', f"%{value}%")]

        self.table = self.build_table(domain)
        box_table = urwid.BoxAdapter(self.table, 24)

        self.pile.contents[-1] = (box_table, self.pile.options('pack', None))

    def build_table(self, domain):
        headers_list = ['id', 'name', 'slug']
        data = self.tenancy_reporter.search_tenants(domain)
        return Table(data, headers_list)

    def set_current_tenant(self):
        self.selected_item = self.table.get_selected_item()
        self.affiliation_coordinator.establish_tenant(self.selected_item['id'])

        self._back()
        main_menu = self.env.holder.original_widget
        main_menu.rebuild()

    def keypress(self, size, key):
        if key in ('enter'):
            self.set_current_tenant()
        return super().keypress(size, key)
