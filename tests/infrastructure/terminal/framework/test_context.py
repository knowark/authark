import urwid
from pytest import fixture
from authark.infrastructure.terminal.framework import Context


def test_context_instantiation(environment):
    class ConcreteContext(Context):
        pass
    context = ConcreteContext()
    assert context is not None
    assert isinstance(context.config, dict)
    assert context.resolver is None
