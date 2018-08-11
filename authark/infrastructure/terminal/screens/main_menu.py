import urwid
from typing import Dict, Callable
from authark.infrastructure.terminal.framework.screen import Screen
from authark.infrastructure.terminal.framework.environment import Environment


class MainMenu(Screen):

    def _build_widget(self) -> urwid.Widget:
        text = urwid.Text(self.name)
        edit = urwid.Edit()

        next_button = urwid.Button("Next", on_press=self.on_next)
        back_button = urwid.Button("Back", on_press=self.on_back)

        widget = urwid.Filler(urwid.Pile(
            [text, edit, next_button, back_button]))

        return widget

    def on_next(self, button):
        pass

    def on_back(self, button):
        self._back()
