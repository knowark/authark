import urwid
import json
from ...framework import Screen, Table


class TenantsDetailsScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_coordinator = self.env.context.resolve(
            'AuthCoordinator')
        self.authark_reporter = self.env.context.resolve(
            'AutharkReporter')

        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'primary_bg')

        footer = urwid.Text([
            "Press (", ("success", "Enter"), ") to save. ",
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        if not self.parent:
            return

        self.selected_item = self.parent.table.get_selected_item()
        username = self.selected_item.get('username', "")
        email = self.selected_item.get('email', "")
        name = self.selected_item.get('name', "")
        gender = self.selected_item.get('gender', "")

        attributes = json.dumps(
            self.selected_item.get('attributes', {}),
            sort_keys=True, indent=2)

        title = "{}: {}".format(self.name, username)

        self.username = urwid.Edit("> ", username)
        self.email = urwid.Edit("> ", email)
        self.name = urwid.Edit("> ", name)
        self.gender = urwid.Edit("> ", gender)
        self.password = urwid.Edit("> ", "")
        self.attributes = urwid.Edit("", attributes, multiline=True)

        body = urwid.Pile([
            urwid.Columns([
                urwid.Text("Username: ", align='center'), self.username]),
            urwid.Columns([
                urwid.Text("Email: ", align='center'), self.email]),
            urwid.Columns([
                urwid.Text("Name: ", align='center'), self.name]),
            urwid.Columns([
                urwid.Text("Gender: ", align='center'), self.gender]),
            urwid.Columns([
                urwid.Text("Password: ", align='center'), self.password]),
            urwid.Columns([
                urwid.Text("Attributes: ", align='center'), self.attributes])
        ])

        body = urwid.Padding(urwid.Filler(body), align='center', width=80)

        frame = urwid.Frame(header=header, body=body, footer=footer)

        widget = urwid.Overlay(
            frame, self.parent,
            align='center', width=('relative', 50),
            valign='middle', height=('relative', 50),
            min_width=20, min_height=9)

        return widget

    # def keypress(self, size, key):
    #     if key == 'meta enter':
    #         self.selected_item['username'] = self.username.edit_text
    #         self.selected_item['email'] = self.email.edit_text
    #         self.selected_item['name'] = self.name.edit_text
    #         self.selected_item['gender'] = self.gender.edit_text

    #         if self.password.edit_text:
    #             self.selected_item['password'] = self.password.edit_text

    #         self.selected_item['attributes'] = json.loads(
    #             self.attributes.edit_text)

    #         self.auth_coordinator.update(self.selected_item)
    #         self._go_back()

    #     if key == 'left':
    #         return super(urwid.WidgetWrap, self).keypress(size, key)
    #     return super().keypress(size, key)

    # def _go_back(self):
    #     self._back()
    #     main_menu = self.env.stack.pop()
    #     main_menu.show_users_screen()
