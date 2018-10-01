import urwid
from pytest import fixture
from authark.infrastructure.config.context import Context
from authark.infrastructure.terminal.framework.environment import Environment
from authark.infrastructure.terminal.framework.screen import Screen
from authark.infrastructure.terminal.framework.table import Table
from authark.infrastructure.terminal.framework.themes import palette


@fixture
def environment(context):
    holder = urwid.WidgetPlaceholder(urwid.SolidFill('/'))
    stack = []  # type: List[urwid.Widget]
    return Environment(
        holder=holder,
        stack=stack,
        context=context)


@fixture
def screen(environment):
    class MockScreen(Screen):
        def _build_widget(self):
            return urwid.Button('Mock')

    return MockScreen('Mock', environment)


@fixture
def table():
    data_list = [
        {'name': 'Esteban', 'age': 29},
        {'name': 'Adriana', 'age': 59},
        {'name': 'Cesar', 'age': 61}
    ]
    headers_list = ['name', 'age']
    return Table(data_list, headers_list)


@fixture
def themes():
    return palette
