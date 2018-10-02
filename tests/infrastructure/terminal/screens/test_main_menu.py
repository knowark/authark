import urwid
from pytest import raises, fixture
from authark.infrastructure.terminal.screens.main_menu import MainMenu
from authark.infrastructure.terminal.screens.users.users import UsersScreen


@fixture
def main_menu(main):
    return MainMenu('MainMenu', main.env)


def test_main_menu_instantiation(main_menu):
    assert main_menu is not None


def test_main_menu_show_users_screen(main_menu):
    main_menu.show_users_screen()
    assert isinstance(main_menu.env.holder.original_widget, UsersScreen)
