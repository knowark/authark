import urwid
from pytest import fixture
from authark.infrastructure.terminal.framework.environment import Environment


@fixture
def environment(context):
    holder = urwid.WidgetPlaceholder(urwid.SolidFill('/'))
    stack = []  # type: List[urwid.Widget]
    return Environment(
        holder=holder,
        stack=stack,
        context=context)


def test_environment_instantiation(environment):
    assert environment is not None
