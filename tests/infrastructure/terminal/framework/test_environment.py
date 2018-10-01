import urwid
from pytest import fixture
from authark.infrastructure.config.context import Context
from authark.infrastructure.terminal.framework.environment import Environment


def test_environment_instantiation(environment):
    assert environment is not None
    assert isinstance(environment.holder, urwid.WidgetPlaceholder)
    assert isinstance(environment.stack, list)
    assert isinstance(environment.context, Context)
