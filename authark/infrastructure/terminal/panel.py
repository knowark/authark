import urwid
from authark.infrastructure.config.context import Context


class Panel:
    """Main Authark's Terminal Application Panel"""

    def __init__(self, context: Context):
        # self.log = urwid.SimpleFocusListWalker([])
        # self.top = urwid.ListBox(self.log)
        self.context = context
        self.top = urwid.Filler(urwid.Text("AUTHARK"), 'top')

        self.loop = urwid.MainLoop(
            self.top,
            palette=[('reversed', 'standout', '')],
            unhandled_input=self._unhandled_input)

    def _unhandled_input(self, key: str):
        if key in ('q', 'Q'):
            self.exit()

    def exit(self):
        raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()
