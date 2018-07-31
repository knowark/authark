import urwid
from authark.infrastructure.terminal.screens import Screen


def launch_users_screen(
        button: urwid.Button, choice: str, top_widget: urwid.Widget):

    top_widget.top_w.original_widget = Screen(header="USERS")
