# from pytest import fixture
# from typing import Dict
# from authark.application.models import (
#     Dominion, Role, Ranking, Resource, Grant,
#     Permission, Policy)
# from authark.application.utilities import ExpressionParser
# from authark.application.services import (
#     TokenService, MemoryTokenService,
#     TenantService, StandardTenantService)
# from authark.application.repositories import (
#     DominionRepository, MemoryDominionRepository,
#     RoleRepository, MemoryRoleRepository,
#     ResourceRepository, MemoryResourceRepository,
#     GrantRepository, MemoryGrantRepository,
#     PermissionRepository, MemoryPermissionRepository,
#     PolicyRepository, MemoryPolicyRepository,
#     RankingRepository, MemoryRankingRepository)


# @fixture
# def dominion_repository() -> DominionRepository:
#     dominions_dict = {
#         "1": Dominion(id='1', name='Data System',
#                       url="https://datasystem.nubark.com")
#     }
#     parser = ExpressionParser()
#     dominion_repository = MemoryDominionRepository(parser)
#     dominion_repository.load(dominions_dict)
#     return dominion_repository


# @fixture
# def role_repository() -> RoleRepository:
#     roles_dict = {
#         "1": Role(id='1', name='admin', dominion_id='1',
#                   description="Service's Administrator")
#     }
#     parser = ExpressionParser()
#     role_repository = MemoryRoleRepository(parser)
#     role_repository.load(roles_dict)
#     return role_repository


# @fixture
# def ranking_repository() -> RankingRepository:
#     rankings_dict = {
#         "1": Ranking(id='1', user_id='1', role_id='1',
#                      description="Service's Administrator")
#     }
#     parser = ExpressionParser()
#     ranking_repository = MemoryRankingRepository(parser)
#     ranking_repository.load(rankings_dict)
#     return ranking_repository


# @fixture
# def resource_repository() -> ResourceRepository:
#     resources_dict = {
#         "1": Resource(id='1', name='employees',
#                       dominion_id='1')
#     }
#     parser = ExpressionParser()
#     resource_repository = MemoryResourceRepository(parser)
#     resource_repository.load(resources_dict)
#     return resource_repository


# @fixture
# def grant_repository() -> GrantRepository:
#     grants_dict = {
#         '001': Grant(id='001', permission_id='001', role_id='1')
#     }
#     parser = ExpressionParser()
#     grant_repository = MemoryGrantRepository(parser)
#     grant_repository.load(grants_dict)
#     return grant_repository


# @fixture
# def permission_repository() -> PermissionRepository:
#     permission_dict = {
#         "001": Permission(id='001', policy_id='001', resource_id='1')
#     }
#     parser = ExpressionParser()
#     permission_repository = MemoryPermissionRepository(parser)
#     permission_repository.load(permission_dict)
#     return permission_repository


# @fixture
# def policy_repository() -> PolicyRepository:
#     policy_dict = {
#         "001": Policy(id='001', name='First Role Only', value="1")
#     }
#     parser = ExpressionParser()
#     policy_repository = MemoryPolicyRepository(parser)
#     policy_repository.load(policy_dict)
#     return policy_repository


# @fixture
# def token_service() -> TokenService:
#     return MemoryTokenService()


# @fixture
# def catalog_service() -> CatalogService:
#     parser = ExpressionParser()
#     return MemoryCatalogService(parser)


# @fixture
# def tenant_service() -> TenantService:
#     return StandardTenantService()


# @fixture
# def provision_service() -> ProvisionService:
#     return MemoryProvisionService()
