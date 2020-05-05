import urwid
import json
from ...framework import Screen, Table


class TenantsDetailsScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'info_bg')

        footer = urwid.Text([
            "Press (", ("success", "Enter"), ") to save. ",
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        if not self.parent:
            return

        self.selected_item = self.parent.table.get_selected_item()
        tenant_id = self.selected_item.get('id', "")
        name = self.selected_item.get('name', "")
        email = self.selected_item.get('email', "")
        active = str(self.selected_item.get('active', ""))
        slug = self.selected_item.get('slug', "")
        location = self.selected_item.get('location', "")

        title = f"{self.name}: {name}"

        self.name_edit = urwid.Edit("> ", name)
        self.email = urwid.Edit("> ", email)
        self.active = urwid.Edit("> ", active)
        self.slug = urwid.Edit("> ", slug)
        self.location = urwid.Edit("> ", location)

        body = urwid.Pile([
            urwid.Columns([
                urwid.Text("Name: ", align='center'), self.name_edit]),
            urwid.Columns([
                urwid.Text("Email: ", align='center'), self.email]),
            urwid.Columns([
                urwid.Text("Active: ", align='center'), self.active]),
            urwid.Columns([
                urwid.Text("Slug: ", align='center'), self.slug]),
            urwid.Columns([
                urwid.Text("Location: ", align='center'), self.location])
        ])

        body = urwid.Padding(urwid.Filler(body), align='center', width=100)

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
            min_width=20, min_height=9)

        return widget


# class TenantsExportScreen(Screen):

#     def _build_widget(self) -> urwid.Widget:
#         self.export_coordinator = self.env.context.resolve(
#             'ExportCoordinator')

#         header = urwid.AttrMap(
#             urwid.Text(self.name, align='center'), 'info_bg')

#         footer = urwid.Text([
#             "Press (", ("success", "Enter"), ") to save. ",
#             "Press (", ("warning", "Esc"), ") to go back. "
#         ])

#         if not self.parent:
#             return

#         tenants_number = len(self.parent.selected_tenants)

#         export_location = 'Export location: "/opt/authark/export"'
#         legend = [
#             'Do you want to export the selected ',
#             ("warning", f'"{tenants_number}" '),
#             'tenants?']

#         body = urwid.Pile([
#             urwid.Text(export_location, align='center'),
#             urwid.Divider(),
#             urwid.Divider(),
#             urwid.Text(legend, align='center')
#         ])

#         body = urwid.Padding(urwid.Filler(body), align='center', width=100)

#         frame = urwid.Frame(header=header, body=body, footer=footer)

#         widget = urwid.Overlay(
#             frame, self.parent,
#             align='center', width=('relative', 50),
#             valign='middle', height=('relative', 50),
#             min_width=20, min_height=9)

#         return widget

#     def keypress(self, size, key):
#         if key in ('enter'):
#             tenant_ids = list(self.parent.selected_tenants)
#             self.export_coordinator.export_tenants(tenant_ids)
#             self._back()

#         return super().keypress(size, key)
