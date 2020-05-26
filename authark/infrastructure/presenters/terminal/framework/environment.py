import urwid
from typing import List
from .context import Context


class Environment:
    def __init__(self,
                 holder: urwid.WidgetPlaceholder,
                 stack: List[urwid.Widget],
                 context: Context) -> None:
        self.holder = holder
        self.stack = stack
        self.context = context
