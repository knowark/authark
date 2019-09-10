from pytest import fixture
from authark.infrastructure.terminal.screens.main_menu import MainMenu
from authark.infrastructure.terminal.screens.policies import (
    PoliciesScreen, PoliciesAddScreen)


@fixture
def policies_add_screen(main):
    policies_add_screen = PoliciesAddScreen('ADD POLICY', main.env, main)
    policies_add_screen.env.stack.append(MainMenu('MainMenu', main.env))
    policies_add_screen.env.stack.append(main)
    return policies_add_screen


def test_policies_add_screen_instance(policies_add_screen):
    assert policies_add_screen is not None


def test_policies_add_screen_keypress_left(policies_add_screen):
    policies_add_screen.keypress((0, 0), "left")
    assert isinstance(
        policies_add_screen.env.holder.original_widget, MainMenu)


def test_policies_add_screen_keypress_enter(policies_add_screen):
    policies_add_screen.keypress((0, 0), "enter")
    assert isinstance(
        policies_add_screen.env.holder.original_widget, PoliciesScreen)
