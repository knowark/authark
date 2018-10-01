import urwid
from authark.infrastructure.terminal.framework.table import Table


def test_table_instantiation(table):
    assert table is not None
