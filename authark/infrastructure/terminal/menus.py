import urwid
from typing import Dict, Callable


class MainMenu(urwid.WidgetWrap):

    def __init__(self, title: str, options: Dict[str, Callable[
            [urwid.Button, str], None]]) -> None:

        title_widget = urwid.AttrMap(
            urwid.Text(title, align='center'), 'heading')
        body = [title_widget, urwid.Divider()]
        for option, callback in options.items():
            button = urwid.Button(option)
            urwid.connect_signal(button, 'click', callback, option)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))

        widget = urwid.Padding(
            urwid.ListBox(urwid.SimpleFocusListWalker(body)),
            left=2, right=2)
        super().__init__(widget)
