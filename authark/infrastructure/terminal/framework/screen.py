import logging
import urwid
from abc import ABC, abstractmethod
from typing import List
from authark.infrastructure.terminal.framework.environment import Environment


class Screen(urwid.WidgetWrap):

    def __init__(self, name: str, env: Environment) -> None:
        self.name = name
        self.env = env
        self.logger = logging.getLogger(__name__)

        widget = self._build_widget()
        super().__init__(widget)

        self.env.holder.original_widget = self

    def _build_widget(self) -> urwid.Widget:
        raise NotImplementedError("Should be implemented by children.")

    def _open_screen(self, screen: 'Screen' = None) -> None:
        self.env.stack.append(self)
        self.env.holder.original_widget = screen
        self.logger.debug("OPEN: %s", self.env.stack)

    def _back(self):
        if self.env.stack:
            previous = self.env.stack.pop()
            self.env.holder.original_widget = previous
        self.logger.debug("BACK: %s", self.env.stack)
