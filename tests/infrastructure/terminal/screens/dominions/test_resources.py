import urwid
from pytest import raises, fixture
from authark.infrastructure.terminal.screens.dominions import DominionsScreen
from authark.infrastructure.terminal.screens.dominions.resources import (
    DominionsResourcesScreen, DominionsAddResourceScreen,
    ResourcesPoliciesScreen, ResourcesAssignPolicyScreen)


@fixture
def dominions_resources_screen(main):
    dominions_screen = DominionsScreen("DOMINIONS", main.env)
    dominions_screen.keypress((0, 0), "S")
    dominions_resources_screen = dominions_screen.env.holder.original_widget
    assert isinstance(dominions_resources_screen, DominionsResourcesScreen)
    return dominions_resources_screen


@fixture
def dominions_add_resource_screen(dominions_resources_screen):
    dominions_resources_screen.keypress((0, 0), "A")
    dominions_add_resource_screen = \
        dominions_resources_screen.env.holder.original_widget
    assert isinstance(dominions_add_resource_screen,
                      DominionsAddResourceScreen)
    return dominions_add_resource_screen


@fixture
def resources_policies_screen(dominions_resources_screen):
    dominions_resources_screen.keypress((0, 0), "P")
    resources_policies_screen = \
        dominions_resources_screen.env.holder.original_widget
    assert isinstance(resources_policies_screen,
                      ResourcesPoliciesScreen)
    return resources_policies_screen


@fixture
def resources_assign_policy_screen(resources_policies_screen):
    resources_policies_screen.keypress((0, 0), "A")
    resources_assign_policy_screen = \
        resources_policies_screen.env.holder.original_widget
    assert isinstance(resources_assign_policy_screen,
                      ResourcesAssignPolicyScreen)
    return resources_assign_policy_screen


def test_dominions_resources_screen_instance(dominions_resources_screen):
    assert dominions_resources_screen is not None


def test_dominions_resources_screen_no_parent(main):
    assert DominionsResourcesScreen(
        'DOMINION RESOURCES', main.env, None) is not None


def test_dominions_resources_screen_keypress(dominions_resources_screen):
    assert dominions_resources_screen.keypress((40, 40), 'F') == 'F'


def test_dominions_add_resource_screen_instance(dominions_add_resource_screen):
    assert dominions_add_resource_screen is not None


def test_dominions_add_resource_screen_keypress_enter(
        dominions_add_resource_screen):
    dominions_add_resource_screen.keypress((0, 0), "enter")
    assert isinstance(dominions_add_resource_screen.env.holder.original_widget,
                      DominionsResourcesScreen)


def test_dominions_add_resource_screen_keypress_left(
        dominions_add_resource_screen):
    dominions_add_resource_screen.keypress((0, 0), "left")
    assert isinstance(dominions_add_resource_screen.env.holder.original_widget,
                      DominionsAddResourceScreen)


def test_resources_policies_screen_instance(resources_policies_screen):
    assert resources_policies_screen is not None


def test_resources_policies_screen_keypress_unhandled(
        resources_policies_screen):
    assert resources_policies_screen.keypress((0, 0), "F") == "F"


def test_resources_policies_screen_no_parent(main):
    assert ResourcesPoliciesScreen(
        'RESOURCE POLICIES', main.env, None) is not None


def test_resources_assign_policy_screen_instance(
        resources_assign_policy_screen):
    assert resources_assign_policy_screen is not None


def test_resources_assign_policy_screen_build_policy_selection(
        resources_assign_policy_screen):
    build_policy_selection = \
        resources_assign_policy_screen._build_policy_selection()
    policies = build_policy_selection.item_list_collector("")
    assert policies[0]["id"] == "1"
    assert build_policy_selection.item_formatter(
        {'name': 'Jhon Jairo'}) == "Jhon Jairo"


def test_resources_assign_policy_screen_add_permission(
        resources_assign_policy_screen):
    resources_assign_policy_screen.policy_selection.selected = {"id": "1"}
    resources_assign_policy_screen.resource = {"id": "1"}
    resources_assign_policy_screen._add_permission(None)
    assert isinstance(
        resources_assign_policy_screen.env.holder.original_widget,
        ResourcesPoliciesScreen)


def test_resources_assign_policy_screen_no_parent(main):
    assert ResourcesAssignPolicyScreen(
        'ASSIGN POLICY', main.env, None) is not None
