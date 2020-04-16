# from pytest import fixture, raises
# from authark.application.models.user import User
# from authark.application.models.credential import Credential
# from authark.application.repositories.memory_model_repositories import (
#     UserRepository, MemoryUserRepository, CredentialRepository, MemoryCredentialRepository)
# from authark.application.utilities import QueryParser
# from authark.application.reporters import ComposingReporter


# def test_composing_reporter_methods():
#     methods = ComposingReporter.__abstractmethods__
#     assert 'list_user_roles' in methods


# def test_composing_reporter_list_user_roles(composing_reporter):
#     user_id = '1'
#     result = composing_reporter.list_user_roles(user_id)
#     assert isinstance(result, list)
#     assert result[0] == {'ranking_id': '1', 'role': 'admin',
#                          'dominion': 'Data Server'}


# def test_composing_reporter_list_user_roles_(composing_reporter):
#     user_id = '1'
#     result = composing_reporter.list_user_roles(user_id)
#     assert isinstance(result, list)
#     assert result[0] == {'ranking_id': '1', 'role': 'admin',
#                          'dominion': 'Data Server'}
