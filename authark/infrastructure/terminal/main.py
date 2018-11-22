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
        self.env = Environment(self.holder, self.stack, self.context)

        self.top = self._build_top(self.holder)
        self.loop = urwid.MainLoop(
            self.top,
            palette=palette,
            unhandled_input=self._unhandled_input)

    def _build_top(self, holder: urwid.Widget) -> urwid.Overlay:
        holder.original_widget = MainMenu("Main Menu", self.env)
        top = urwid.Overlay(
            holder, urwid.SolidFill('\N{MEDIUM SHADE}'),
            align='center', width=('relative', 95),
            valign='middle', height=('relative', 95),
            min_width=20, min_height=9)
        return top

    def _unhandled_input(self, key: str):
        if key == 'meta q':
            self.exit(key)

    def exit(self, key: str):
        raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()
