import urwid
from pytest import raises, fixture
from authark.infrastructure.terminal.screens.main_menu import MainMenu
from authark.infrastructure.terminal.screens.users import UsersScreen
from authark.infrastructure.terminal.screens.dominions import DominionsScreen
from authark.infrastructure.terminal.screens.tenants import TenantsScreen


@fixture
def main_menu(main):
    return MainMenu('MainMenu', main.env)


def test_rebuild_function(main_menu):
    screen = main_menu.rebuild()
    assert isinstance(main_menu.env.holder.original_widget, MainMenu)


def test_main_menu_instantiation(main_menu):
    assert main_menu is not None


def test_main_menu_show_users_screen(main_menu):
    main_menu.show_users_screen()
    assert isinstance(main_menu.env.holder.original_widget, UsersScreen)


def test_main_menu_show_dominions_screen(main_menu):
    main_menu.show_dominions_screen()
    assert isinstance(main_menu.env.holder.original_widget, DominionsScreen)


def test_main_menu_show_tenants_screen(main_menu):
    main_menu.show_tenants_screen()
    assert isinstance(main_menu.env.holder.original_widget, TenantsScreen)


def test_main_menu_keypress_tenant_screen(main_menu):
    main_menu.keypress((0, 0), "T")
    assert isinstance(main_menu.env.holder.original_widget, TenantsScreen)


def test_main_menu_keypress_unhandled(main_menu):
    assert main_menu.keypress((0, 0), "F") == "F"
