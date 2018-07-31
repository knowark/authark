import urwid


class Screen(urwid.WidgetWrap):

    def __init__(self, header: str):
        header = urwid.AttrMap(urwid.Text(header, align='center'), 'titlebar')

        footer = urwid.Text([
            "Press (", ("add button", "A"), ") to add a new record. ",
            "Press (", ("update button", "U"), ") to update a record. ",
            "Press (", ("remove button", "R"), ") to remove a record. "
        ])

        # Create the actual quote box
        body_text = urwid.Text("Here comes the list!")
        body_filler = urwid.Filler(body_text, valign='top', top=1, bottom=1)
        body_padding = urwid.Padding(body_filler, left=1, right=1)
        body = urwid.LineBox(body_padding)

        frame = urwid.Frame(header=header, body=body, footer=footer)

        super().__init__(frame)
