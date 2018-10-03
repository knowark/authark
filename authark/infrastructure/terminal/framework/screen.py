import urwid
from abc import ABC, abstractmethod
from typing import List
from authark.infrastructure.terminal.framework.environment import Environment


class Screen(urwid.WidgetWrap):

    def __init__(self, name: str, env: Environment,
                 parent: 'Screen' = None) -> None:
        self.name = name
        self.env = env
        self.parent = parent

        widget = self._build_widget()
        super().__init__(widget)

        self.env.holder.original_widget = self

    def _build_widget(self) -> urwid.Widget:
        raise NotImplementedError(
            "The 'Screen' class defines the interface that all "
            "browsable screens should follow. Please inherit from "
            "'Screen' and implement the '_build_widget' method.")

    def _open_screen(self, screen: 'Screen' = None) -> None:
        self.env.stack.append(self)
        self.env.holder.original_widget = screen

    def _back(self):
        if self.env.stack:
            previous = self.env.stack.pop()
            self.env.holder.original_widget = previous

    def keypress(self, size, key):
        if key in ['esc', 'left']:
            return self._back()
        return super().keypress(size, key)
