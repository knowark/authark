# import urwid
# from pytest import raises, fixture
# from authark.application.models import AuthError
# from authark.infrastructure.terminal.framework import Screen, Table
# from authark.infrastructure.terminal.screens.main_menu import MainMenu
# from authark.infrastructure.terminal.screens.users import (
#     UsersScreen, UsersAddScreen, UsersDeleteScreen, UsersCredentialsScreen)
# from authark.infrastructure.terminal.screens.users.users_actions import (
#     UsersUpdateScreen)


# class MockParent(Screen):
#     def __init__(self):
#         self.table = Table([
#             {'id': '1', 'username': 'eecheverry', 'password': '123'}
#         ], ['id', 'username', 'password'])
#         self.table.keypress(None, 'down')


# @fixture
# def users_add_screen(main):
#     return UsersAddScreen('USERS ADD', main.env)


# @fixture
# def users_delete_screen(main):
#     return UsersDeleteScreen('USERS DELETE', main.env, MockParent())


# @fixture
# def users_credentials_screen(main):
#     return UsersCredentialsScreen('USERS CREDENTIALS', main.env, MockParent())


# @fixture
# def users_update_screen(main):
#     users_screen = UsersScreen('USERS', main.env)
#     users_screen.pile.focus_position = 1
#     users_screen.keypress((0, 0), 'U')
#     users_update_screen = users_screen.env.holder.original_widget
#     users_update_screen.env.stack.pop()
#     users_update_screen.env.stack.append(MainMenu('MainMenu', main.env))
#     users_update_screen.env.stack.append(users_screen)
#     return users_update_screen


# def test_users_add_screen_instantiation(users_add_screen):
#     assert users_add_screen is not None


# def test_users_add_screen_keypress(main, users_add_screen):
#     called = False

#     class MockMainMenu(Screen):
#         def show_users_screen(self):
#             nonlocal called
#             called = True

#         def _build_widget(self):
#             pass

#     users_add_screen.env.stack = [MockMainMenu(
#         'Mock', main.env), urwid.Text('Mock')]
#     users_add_screen.username.edit_text = 'jplozano'
#     users_add_screen.email.edit_text = 'jplozano@example.com'
#     users_add_screen.password.edit_text = '123'

#     result = users_add_screen.keypress((40, 40), 'ctrl')
#     assert result == 'ctrl'

#     users_add_screen.keypress((40, 40), 'enter')

#     assert len(users_add_screen.auth_coordinator
#                .user_repository.data['knowark']) == 2
#     assert called

#     result = users_add_screen.keypress((40, 40), 'left')
#     assert result == 'left'


# def test_users_delete_screen_instantiation(users_delete_screen):
#     assert users_delete_screen is not None


# def test_users_delete_screen_instantiation_no_parent(main):
#     users_delete_screen = UsersDeleteScreen('USERS DELETE', main.env, None)
#     assert users_delete_screen._build_widget() is None


# def test_users_delete_screen_keypress(main, users_delete_screen):
#     called = False

#     class MockMainMenu(Screen):
#         def show_users_screen(self):
#             nonlocal called
#             called = True

#         def _build_widget(self):
#             pass

#     users_delete_screen.env.stack = [MockMainMenu(
#         'Mock', main.env), urwid.Text('Mock')]

#     result = users_delete_screen.keypress((40, 40), 'ctrl')
#     assert result == 'ctrl'

#     users_delete_screen.keypress((40, 40), 'enter')

#     assert len(users_delete_screen.auth_coordinator
#                .user_repository.data['knowark']) == 0
#     assert called


# def test_users_credentials_screen_instantiation(users_credentials_screen):
#     assert users_credentials_screen is not None


# def test_users_credentials_screen_instantiation_no_parent(main):
#     users_credentials_screen = UsersCredentialsScreen(
#         'USERS CREDENTIALS', main.env, None)
#     assert users_credentials_screen._build_widget() is None


# def test_users_update_screen_no_parent(main):
#     assert UsersUpdateScreen(
#         'UPDATE USER', UsersScreen('USERS UPDATE', main.env).env, None
#     )is not None


# def test_users_update_screen_instantiation(users_update_screen):
#     assert users_update_screen is not None


# def test_users_update_screen_keypress_enter_with_password(users_update_screen):
#     users_update_screen.password.edit_text = "MY_PASSWORD"
#     users_update_screen.keypress((0, 0), "meta enter")
#     auth_coordinator = users_update_screen.auth_coordinator
#     response = auth_coordinator.authenticate(
#         "eecheverry", "MY_PASSWORD", "ALL")
#     assert response["refresh_token"] is not None
#     assert response["access_token"] is not None


# def test_users_update_screen_keypress_enter_without_password(
#         users_update_screen):
#     with raises(AuthError):
#         users_update_screen.password.edit_text = ""
#         users_update_screen.keypress((0, 0), "meta enter")
#         auth_coordinator = users_update_screen.auth_coordinator
#         auth_coordinator.authenticate(
#             "eecheverry", "MY_PASSWORD", "ALL")


# def test_users_update_screen_keypress_left(users_update_screen):
#     users_update_screen.keypress((0, 0), "left")
#     assert isinstance(
#         users_update_screen.env.holder.original_widget, MainMenu)
