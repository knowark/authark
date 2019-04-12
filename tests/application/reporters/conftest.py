from pytest import fixture, raises
from authark.application.models import (
    User, Credential, Dominion, Role, Ranking,
    Policy, Resource, Permission, Grant)
from authark.application.utilities import ExpressionParser
from authark.application.repositories import (
    UserRepository, MemoryUserRepository,
    CredentialRepository, MemoryCredentialRepository,
    DominionRepository, MemoryDominionRepository,
    RoleRepository, MemoryRoleRepository,
    RankingRepository, MemoryRankingRepository,
    PolicyRepository, MemoryPolicyRepository,
    ResourceRepository, MemoryResourceRepository,
    PermissionRepository, MemoryPermissionRepository,
    GrantRepository, MemoryGrantRepository)
from authark.application.services import (
    CatalogService, MemoryCatalogService, Tenant)
from authark.application.reporters import (
    AutharkReporter, StandardAutharkReporter,
    ComposingReporter, StandardComposingReporter,
    TenancyReporter, StandardTenancyReporter)


@fixture
def user_repository() -> UserRepository:
    parser = ExpressionParser()
    user_repository = MemoryUserRepository(parser)
    user_repository.load({
        "valenep": User(id='1', username='valenep', email='valenep@gmail.com'),
        "tebanep": User(id='2', username='tebanep', email='tebanep@gmail.com'),
        "gabeche": User(id='3', username='gabeche', email='gabeche@gmail.com')
    })
    return user_repository


@fixture
def credential_repository() -> CredentialRepository:
    credentials_dict = {
        "1": Credential(id='1', user_id='1', value="PASS1"),
        "2": Credential(id='2', user_id='2', value="PASS2"),
        "3": Credential(id='3', user_id='3', value="PASS3"),
    }
    parser = ExpressionParser()
    credential_repository = MemoryCredentialRepository(parser)
    credential_repository.load(credentials_dict)
    return credential_repository


@fixture
def dominion_repository() -> DominionRepository:
    dominions_dict = {
        "1": Dominion(id='1', name='Data Server',
                      url="https://dataserver.nubark.com")
    }
    parser = ExpressionParser()
    dominion_repository = MemoryDominionRepository(parser)
    dominion_repository.load(dominions_dict)
    return dominion_repository


@fixture
def role_repository() -> RoleRepository:
    roles_dict = {
        "1": Role(id='1', name='admin', dominion_id='1',
                  description="Service's Administrator")
    }
    parser = ExpressionParser()
    role_repository = MemoryRoleRepository(parser)
    role_repository.load(roles_dict)
    return role_repository


@fixture
def ranking_repository() -> RankingRepository:
    rankings_dict = {
        "1": Ranking(id='1', user_id='1', role_id='1',
                     description="Service's Administrator")
    }
    parser = ExpressionParser()
    ranking_repository = MemoryRankingRepository(parser)
    ranking_repository.load(rankings_dict)
    return ranking_repository


@fixture
def policy_repository() -> PolicyRepository:
    policy_dict = {
        "1": Policy(id='1', name="Administrators Only", value="admin")
    }
    parser = ExpressionParser()
    policy_repository = MemoryPolicyRepository(parser)
    policy_repository.load(policy_dict)
    return policy_repository


@fixture
def resource_repository() -> ResourceRepository:
    resource_dict = {
        "1": Resource(id='1', name="products", dominion_id="001")
    }
    parser = ExpressionParser()
    resource_repository = MemoryResourceRepository(parser)
    resource_repository.load(resource_dict)
    return resource_repository


@fixture
def permission_repository() -> PermissionRepository:
    permissions_dict = {
        "1": Permission(id='1', resource_id='1', policy_id='1')
    }
    parser = ExpressionParser()
    permission_repository = MemoryPermissionRepository(parser)
    permission_repository.load(permissions_dict)
    return permission_repository


@fixture
def grant_repository() -> GrantRepository:
    grants_dict = {
        "1": Grant(id='1', role_id='1', permission_id='1')
    }
    parser = ExpressionParser()
    grant_repository = MemoryGrantRepository(parser)
    grant_repository.load(grants_dict)
    return grant_repository


@fixture
def catalog_service() -> CatalogService:
    parser = ExpressionParser()
    catalog_service = MemoryCatalogService(parser)
    catalog_service.catalog = {
        "1": Tenant(id='1', name="Davivienda")
    }
    return catalog_service


@fixture
def authark_reporter(
        user_repository, credential_repository,
        dominion_repository, role_repository, policy_repository,
        resource_repository
) -> AutharkReporter:
    return StandardAutharkReporter(user_repository, credential_repository,
                                   dominion_repository, role_repository,
                                   policy_repository, resource_repository)


@fixture
def composing_reporter(
        dominion_repository, role_repository, ranking_repository,
        resource_repository, policy_repository, permission_repository,
        grant_repository
) -> ComposingReporter:
    return StandardComposingReporter(
        dominion_repository, role_repository, ranking_repository,
        resource_repository, policy_repository, permission_repository,
        grant_repository)


@fixture
def tenancy_reporter(catalog_service) -> TenancyReporter:
    return StandardTenancyReporter(catalog_service)
