import urwid
from pytest import fixture
from authark.infrastructure.config.context import Context
from authark.infrastructure.terminal.framework.environment import Environment
from authark.infrastructure.terminal.framework.screen import Screen


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
            pass

    return MockScreen('Mock', environment)
