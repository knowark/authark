import urwid
from pytest import raises, fixture
from authark.infrastructure.terminal.screens.policies import PoliciesScreen
from authark.infrastructure.terminal.screens.policies.policies_actions import (
    PoliciesAddScreen)


@fixture
def policies_screen(main):
    return PoliciesScreen('USERS', main.env)


def test_policies_screen_instantiation(policies_screen):
    assert policies_screen is not None


def test_policies_screen_key_press(policies_screen):
    policies_screen.keypress((0, 0), "A")
    assert isinstance(
        policies_screen.env.holder.original_widget, PoliciesAddScreen)
    unhandled = policies_screen.keypress((40, 40), 'F')
    assert unhandled == 'F'
