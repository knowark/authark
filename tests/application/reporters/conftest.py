# from pytest import fixture, raises
# from authark.application.models import (
#     User, Credential, Dominion, Role, Ranking)
# from authark.application.utilities import (
#     QueryParser, Tenant, StandardTenantProvider)
# from authark.application.repositories import (
#     UserRepository, MemoryUserRepository,
#     CredentialRepository, MemoryCredentialRepository,
#     DominionRepository, MemoryDominionRepository,
#     RoleRepository, MemoryRoleRepository,
#     RankingRepository, MemoryRankingRepository)
# from authark.application.reporters import (
#     AutharkReporter, StandardAutharkReporter,
#     ComposingReporter, StandardComposingReporter)


# @fixture
# def user_repository() -> UserRepository:
#     tenant_provider = StandardTenantProvider(Tenant(name="Default"))
#     parser = QueryParser()
#     user_repository = MemoryUserRepository(parser, tenant_provider)
#     user_repository.load({
#         "default": {
#             "valenep": User(id='1', username='valenep',
#                             email='valenep@gmail.com'),
#             "tebanep": User(id='2', username='tebanep',
#                             email='tebanep@gmail.com'),
#             "gabeche": User(id='3', username='gabeche',
#                             email='gabeche@gmail.com')
#         }
#     })
#     return user_repository


# @fixture
# def credential_repository() -> CredentialRepository:
#     tenant_provider = StandardTenantProvider(Tenant(name="Default"))
#     credentials_dict = {
#         "default": {
#             "1": Credential(id='1', user_id='1', value="PASS1"),
#             "2": Credential(id='2', user_id='2', value="PASS2"),
#             "3": Credential(id='3', user_id='3', value="PASS3"),
#         }
#     }
#     parser = QueryParser()
#     credential_repository = MemoryCredentialRepository(parser, tenant_provider)
#     credential_repository.load(credentials_dict)
#     return credential_repository


# @fixture
# def dominion_repository() -> DominionRepository:
#     tenant_provider = StandardTenantProvider(Tenant(name="Default"))
#     dominions_dict = {
#         "default": {
#             "1": Dominion(id='1', name='Data Server',
#                           url="https://dataserver.nubark.com")
#         }
#     }
#     parser = QueryParser()
#     dominion_repository = MemoryDominionRepository(parser, tenant_provider)
#     dominion_repository.load(dominions_dict)
#     return dominion_repository


# @fixture
# def role_repository() -> RoleRepository:
#     tenant_provider = StandardTenantProvider(Tenant(name="Default"))
#     roles_dict = {
#         "default": {
#             "1": Role(id='1', name='admin', dominion_id='1',
#                       description="Service's Administrator")
#         }
#     }
#     parser = QueryParser()
#     role_repository = MemoryRoleRepository(parser, tenant_provider)
#     role_repository.load(roles_dict)
#     return role_repository


# @fixture
# def ranking_repository() -> RankingRepository:
#     tenant_provider = StandardTenantProvider(Tenant(name="Default"))
#     rankings_dict = {
#         "default": {
#             "1": Ranking(id='1', user_id='1', role_id='1',
#                          description="Service's Administrator")
#         }
#     }
#     parser = QueryParser()
#     ranking_repository = MemoryRankingRepository(parser, tenant_provider)
#     ranking_repository.load(rankings_dict)
#     return ranking_repository


# @fixture
# def authark_reporter(
#         user_repository, credential_repository,
#         dominion_repository, role_repository
# ) -> AutharkReporter:
#     return StandardAutharkReporter(user_repository, credential_repository,
#                                    dominion_repository, role_repository)


# @fixture
# def composing_reporter(
#         dominion_repository, role_repository, ranking_repository
# ) -> ComposingReporter:
#     return StandardComposingReporter(
#         dominion_repository, role_repository, ranking_repository)
