import urwid
from typing import List
from collections import OrderedDict
from authark.infrastructure.config.context import Context
from authark.infrastructure.terminal.framework.themes import palette
from authark.infrastructure.terminal.framework.environment import Environment
from authark.infrastructure.terminal.screens.main_menu import MainMenu


class Main:
    """Main Authark's Terminal Application"""

    def __init__(self, context: Context) -> None:
        self.context = context
        self.holder = urwid.WidgetPlaceholder(urwid.SolidFill('/'))
        self.stack = []  # type: List[urwid.Widget]
        self.env = Environment(self.holder, self.stack)

        self.top = self._build_top(self.holder)
        self.loop = urwid.MainLoop(
            self.top,
            palette=palette,
            unhandled_input=self._unhandled_input)
        # self._set_main_menu()

    def _build_top(self, holder: urwid.Widget) -> urwid.Overlay:
        content = MainMenu("Main Menu", self.env)
        top = urwid.Overlay(
            content, urwid.SolidFill('\N{MEDIUM SHADE}'),
            align='center', width=('relative', 95),
            valign='middle', height=('relative', 95),
            min_width=20, min_height=9)
        return top

    def _unhandled_input(self, key: str):
        if key in ('q', 'Q'):
            self.exit(key)

    def _set_main_menu(self):
        main_menu = MainMenu("AUTHARK", self._get_options())
        self.holder.original_widget = main_menu

    def _get_options(self):
        return OrderedDict([
            ("USERS", self.option_callback),
            ("ROLES", self.option_callback),
            ("GROUPS", self.option_callback),
            ("PROVIDERS", self.option_callback)
        ])

    def option_callback(self, button: urwid.Button, choice: str):
        response = urwid.Text([u'You chose ', choice, u'\n'])
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', self.exit)
        self.holder.original_widget = urwid.Filler(
            urwid.Pile([response, urwid.AttrMap(
                done, None, focus_map='reversed')]))

    def exit(self, key: str):
        raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()
