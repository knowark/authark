import urwid
from pytest import fixture
from authark.infrastructure.terminal.framework import (
    palette, Environment, Screen, Table, Selection)


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


@fixture
def selection():
    def item_list_collector(x): return ['A', 'B', 'C']

    def item_formatter(x): return str(x)

    return Selection('Items', item_list_collector, item_formatter)
