import urwid
from functools import partial
from collections import OrderedDict
from authark.infrastructure.config.context import Context
from authark.infrastructure.terminal.menus import MainMenu
from authark.infrastructure.terminal import routes
from authark.infrastructure.terminal.themes import palette


class Panel:
    """Main Authark's Terminal Application Panel"""

    def __init__(self, context: Context):
        self.context = context
        self.top = self._build_top()
        self.loop = urwid.MainLoop(
            self.top,
            palette=palette,
            unhandled_input=self._unhandled_input)
        self._set_main_menu()

    def _build_top(self) -> urwid.Overlay:
        placeholder = urwid.WidgetPlaceholder(urwid.SolidFill())
        top = urwid.Overlay(
            placeholder, urwid.SolidFill('\N{MEDIUM SHADE}'),
            align='center', width=('relative', 90),
            valign='middle', height=('relative', 90),
            min_width=20, min_height=9)
        return top

    def _set_main_menu(self):
        main_menu = MainMenu("AUTHARK", self._get_options())
        self.top.top_w.original_widget = main_menu

    def _get_options(self):
        return OrderedDict([
            ("USERS", partial(routes.launch_users_screen,
                              top_widget=self.top)),
            ("ROLES", self.option_callback),
            ("GROUPS", self.option_callback),
            ("PROVIDERS", self.option_callback)
        ])

    def _unhandled_input(self, key: str):
        if key in ('q', 'Q'):
            self.exit(key)

    def option_callback(self, button: urwid.Button, choice: str):
        response = urwid.Text([u'You chose ', choice, u'\n'])
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', self.exit)
        self.top.top_w.original_widget = urwid.Filler(
            urwid.Pile([response, urwid.AttrMap(
                done, None, focus_map='reversed')]))

    def exit(self, key: str):
        raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()
