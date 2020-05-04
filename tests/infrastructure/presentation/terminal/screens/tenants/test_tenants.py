# import urwid
# from pytest import raises, fixture
# from authark.infrastructure.terminal.framework import Table, Screen
# from authark.infrastructure.terminal.screens.main_menu import MainMenu
# from authark.infrastructure.terminal.screens.tenants import TenantsScreen
# from authark.infrastructure.terminal.screens.tenants.tenants_actions import (
#     TenantsDetailsScreen)
# # from authark.infrastructure.terminal.screens.tenants.tenants_actions import(
# #     TenantsExportScreen)


# class MockParent(Screen):
#     def __init__(self):
#         self.dominion = {'id': '1', 'name': 'Data Server',
#                          'url': 'https://dataserver.nubark.cloud'}
#         self.table = Table([
#             {'id': '1', 'name': 'admin', 'description': 'Administrator'}
#         ], ['id', 'name', 'description'])
#         self.table.keypress(None, 'down')


# @fixture
# def tenants_screen(main):
#     return TenantsScreen('TENANTS', main.env)


# @fixture
# def tenants_screen_with_parent(main):
#     return TenantsScreen('TENANTS', main.env, MockParent())


# def test_tenants_screen_instantiation(tenants_screen):
#     assert tenants_screen is not None


# def test_tenants_show_details_screen(tenants_screen):
#     tenants_screen.table = Table([],  [])
#     tenants_screen.show_details_screen()
#     assert isinstance(
#         tenants_screen.env.holder.original_widget, TenantsDetailsScreen)


# # def test_tenants_show_export_screen(tenants_screen):
# #     tenants_screen.selected_tenants = ["mock_tenant"]
# #     tenants_screen.show_export_screen()
# #     assert isinstance(
# #         tenants_screen.env.holder.original_widget, TenantsExportScreen)

# def test_tenants_toggle_tenant(tenants_screen):
#     tenants_screen.selected_tenants = set(["mock_tenant"])
#     tenants_screen.toggle_tenant(None, None, "new_tenant")
#     assert tenants_screen.selected_tenants == set(
#         ["mock_tenant", "new_tenant"])
#     tenants_screen.toggle_tenant(None, None, "new_tenant")
#     assert tenants_screen.selected_tenants == set(["mock_tenant"])


# def test_tenants_set_current_tenant(tenants_screen_with_parent, main):
#     tenants_screen_with_parent.env.holder.original_widget = MainMenu(
#         "Main Menu", main.env)
#     tenants_screen_with_parent.set_current_tenant()
#     assert tenants_screen_with_parent.session_coordinator.get_tenant()[
#         "name"] == "Knowark"


# def test_tenants_keypress(tenants_screen_with_parent, main):
#     tenants_screen_with_parent.pile.focus_position = 2
#     tenants_screen_with_parent.env.holder.original_widget = MainMenu(
#         "Main Menu", main.env)
#     tenants_screen_with_parent.keypress((0, 0), 'enter')
#     assert tenants_screen_with_parent.session_coordinator.get_tenant()[
#         "name"] == "Knowark"
#     tenants_screen_with_parent.keypress((0, 0), 'D')
#     assert isinstance(tenants_screen_with_parent.env.holder.original_widget,
#                       TenantsDetailsScreen)


# def test_tenants_keypress_no_focus(tenants_screen_with_parent, main):
#     tenants_screen_with_parent.pile.focus_position = 1
#     unhandled = tenants_screen_with_parent.keypress((40, 40), 'F')
#     assert unhandled == 'F'
