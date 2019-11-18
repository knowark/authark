import urwid
from ...framework import Table, Screen
from .roles import DominionsRolesScreen


class DominionsScreen(Screen):

    def _build_widget(self) -> urwid.Widget:
        self.auth_reporter = self.env.context.resolve(
            'AutharkReporter')
        header = urwid.AttrMap(
            urwid.Text(self.name, align='center'), 'secondary_bg')

        footer = urwid.Text([
            "Press (", ("success", "A"), ") to add a new record. ",
            "Press (", ("light", "R"), ") to show roles. ",
            "Press (", ("warning", "Esc"), ") to go back. "
        ])

        headers_list = ['name', 'url']
        data = self.auth_reporter.search_dominions([])

        self.table = Table(data, headers_list)
        body = self.table

        frame = urwid.Frame(header=header, body=body, footer=footer)

        return frame

    def show_roles_screen(self):
        screen = DominionsRolesScreen('DOMINION ROLES', self.env, self)
        return self._open_screen(screen)

    def keypress(self, size, key):
        if key in ('a', 'A'):
            screen = DominionsAddScreen('ADD DOMINION', self.env, self)
            return self._open_screen(screen)
        if key in ('r', 'R', 'enter') and len(self.table):
            return self.show_roles_screen()
        return super().keypress(size, key)


class DominionsAddScreen(Screen):

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
        self.url = urwid.Edit()

        body = urwid.Pile([
            urwid.Columns([
                urwid.Text("Name: ", align='center'), self.name]),
            urwid.Columns([
                urwid.Text("URL: ", align='center'), self.url])
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
            dominion_dict = {}
            dominion_dict['name'] = self.name.edit_text
            dominion_dict['url'] = self.url.edit_text
            dominion = self.management_coordinator.create_dominion(
                dominion_dict)
            self._go_back()
        if key == 'left':
            return super(urwid.WidgetWrap, self).keypress(size, key)
        return super().keypress(size, key)

    def _go_back(self):
        self._back()
        main_menu = self.env.stack.pop()
        main_menu.show_dominions_screen()
