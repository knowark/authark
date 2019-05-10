import urwid
from typing import List
from collections import OrderedDict
from authark.infrastructure.terminal.framework.context import Context
from authark.infrastructure.terminal.framework.themes import palette
from authark.infrastructure.terminal.framework.environment import Environment
from authark.infrastructure.terminal.screens.main_menu import MainMenu


class Main:
    """Main Authark's Terminal Application"""

    def __init__(self, context: Context) -> None:
        self.context = context
        self.holder = urwid.WidgetPlaceholder(urwid.SolidFill('/'))
        self.stack: List[urwid.Widget] = []
        self.env = Environment(self.holder, self.stack, self.context)

        self.top = self._build_top(self.holder)
        self.loop = urwid.MainLoop(
            self.top,
            palette=palette,
            unhandled_input=self._unhandled_input)

    def _build_top(self, holder: urwid.Widget) -> urwid.Overlay:
        self._setup_initial_tenant()
        holder.original_widget = MainMenu("Main Menu", self.env)
        top = urwid.Overlay(
            holder, urwid.SolidFill('\N{MEDIUM SHADE}'),
            align='center', width=('relative', 95),
            valign='middle', height=('relative', 95),
            min_width=20, min_height=9)
        return top

    def _setup_initial_tenant(self) -> None:
        self.tenancy_supplier = self.env.context.resolve('TenantSupplier')
        self.session_coordinator = self.env.context.resolve(
            'SessionCoordinator')
        first_tenant = self.tenancy_supplier.search_tenants([])[0]
        self.session_coordinator.set_tenant(first_tenant)

    def _unhandled_input(self, key: str):
        if key == 'meta q':
            self.exit(key)

    def exit(self, key: str):
        raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()
