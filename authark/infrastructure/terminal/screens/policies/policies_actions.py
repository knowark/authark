import urwid
from ...framework import Screen, Table


class PoliciesAddScreen(Screen):

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
        self.type = urwid.Edit()
        self.value = urwid.Edit()

        body = urwid.Pile([
            urwid.Columns([
                urwid.Text("Name: ", align='center'), self.name]),
            urwid.Columns([
                urwid.Text("Type: ", align='center'), self.type]),
            urwid.Columns([
                urwid.Text("Value: ", align='center'), self.value])
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
            policy_dict = {}
            policy_dict['name'] = self.name.edit_text
            policy_dict['type'] = self.type.edit_text
            policy_dict['value'] = self.value.edit_text
            policy = self.management_coordinator.create_policy(
                policy_dict)
            self._go_back()
        if key == 'left':
            return super(urwid.WidgetWrap, self).keypress(size, key)
        return super().keypress(size, key)

    def _go_back(self):
        self._back()
        main_menu = self.env.stack.pop()
        main_menu.show_policies_screen()
