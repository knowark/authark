import urwid


def launch_users_screen(
        button: urwid.Button, choice: str, top_widget: urwid.Widget):
    response = urwid.Text(['SUPER USERS ', choice, '\n'])
    done = urwid.Button('Ok')
    # urwid.connect_signal(done, 'click', self.exit)
    top_widget.top_w.original_widget = urwid.Filler(
        urwid.Pile([response, urwid.AttrMap(
            done, None, focus_map='reversed')]))
