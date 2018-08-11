import urwid
import logging
from typing import List


class Environment:
    def __init__(self,
                 holder: urwid.WidgetPlaceholder,
                 stack: List[urwid.Widget]) -> None:
        self.holder = holder
        self.stack = stack
