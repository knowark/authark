# from pytest import fixture, raises
# from authark.application.models.user import User
# from authark.application.models.credential import Credential
# from authark.application.repositories.memory_model_repositories import (
#     UserRepository, MemoryUserRepository, CredentialRepository, MemoryCredentialRepository)
# from authark.application.utilities import QueryParser
# from authark.application.informers.authark_informer import (
#     AutharkInformer)


# # def test_authark_informer_methods():
# #     methods = AutharkInformer.__abstractmethods__
# #     assert 'search_users' in methods
# #     assert 'search_credentials' in methods


# async def test_memory_authark_informer_search_users_all(authark_informer):
#     domain = []
#     users = await authark_informer.search_users(domain)

#     assert len(users) == 3


# async def test_memory_authark_informer_search_credentials_all(authark_informer):
#     domain = []
#     credentials = await authark_informer.search_credentials(domain)

#     assert len(credentials) == 3


# async def test_memory_authark_informer_search_dominions_all(authark_informer):
#     domain = []
#     dominions = await authark_informer.search_dominions(domain)

#     assert len(dominions) == 1


# async def test_memory_authark_informer_search_roles_all(authark_informer):
#     domain = []
#     roles = await authark_informer.search_roles(domain)

#     assert len(roles) == 1
