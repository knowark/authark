import urwid
from pytest import raises, fixture
from authark.infrastructure.terminal.framework import Table
from authark.infrastructure.terminal.screens.tenants import TenantsScreen
from authark.infrastructure.terminal.screens.tenants.tenants_actions import (
    TenantsDetailsScreen, TenantsExportScreen)


@fixture
def tenants_screen(main):
    return TenantsScreen('USERS', main.env)


def test_tenants_screen_instantiation(tenants_screen):
    assert tenants_screen is not None


# def test_tenants_show_details_screen(tenants_screen):
#     tenants_screen.show_details_screen()
#     tenants_screen.table = Table([],  ['', 'id', 'name', 'slug'])
#     assert isinstance(
#         tenants_screen.env.holder.original_widget, TenantsDetailsScreen)


# def test_tenants_show_export_screen(tenants_screen):
#     tenants_screen.selected_tenants = ["mock_tenant"]
#     tenants_screen.table = Table([],  ['', 'id', 'name', 'slug'])
#     tenants_screen.show_export_screen()
#     assert isinstance(
#         tenants_screen.env.holder.original_widget, TenantsExportScreen)
