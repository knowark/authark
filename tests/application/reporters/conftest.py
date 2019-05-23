from pytest import fixture, raises
from authark.application.models import (
    User, Credential, Dominion, Role, Ranking,
    Policy, Resource, Permission, Grant)
from authark.application.utilities import (
    ExpressionParser, Tenant, StandardTenantProvider)
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
from authark.application.reporters import (
    AutharkReporter, StandardAutharkReporter,
    ComposingReporter, StandardComposingReporter)


@fixture
def user_repository() -> UserRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    parser = ExpressionParser()
    user_repository = MemoryUserRepository(parser, tenant_provider)
    user_repository.load({
        "default": {
            "valenep": User(id='1', username='valenep',
                            email='valenep@gmail.com'),
            "tebanep": User(id='2', username='tebanep',
                            email='tebanep@gmail.com'),
            "gabeche": User(id='3', username='gabeche',
                            email='gabeche@gmail.com')
        }
    })
    return user_repository


@fixture
def credential_repository() -> CredentialRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    credentials_dict = {
        "default": {
            "1": Credential(id='1', user_id='1', value="PASS1"),
            "2": Credential(id='2', user_id='2', value="PASS2"),
            "3": Credential(id='3', user_id='3', value="PASS3"),
        }
    }
    parser = ExpressionParser()
    credential_repository = MemoryCredentialRepository(parser, tenant_provider)
    credential_repository.load(credentials_dict)
    return credential_repository


@fixture
def dominion_repository() -> DominionRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    dominions_dict = {
        "default": {
            "1": Dominion(id='1', name='Data Server',
                          url="https://dataserver.nubark.com")
        }
    }
    parser = ExpressionParser()
    dominion_repository = MemoryDominionRepository(parser, tenant_provider)
    dominion_repository.load(dominions_dict)
    return dominion_repository


@fixture
def role_repository() -> RoleRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    roles_dict = {
        "default": {
            "1": Role(id='1', name='admin', dominion_id='1',
                      description="Service's Administrator")
        }
    }
    parser = ExpressionParser()
    role_repository = MemoryRoleRepository(parser, tenant_provider)
    role_repository.load(roles_dict)
    return role_repository


@fixture
def ranking_repository() -> RankingRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    rankings_dict = {
        "default": {
            "1": Ranking(id='1', user_id='1', role_id='1',
                         description="Service's Administrator")
        }
    }
    parser = ExpressionParser()
    ranking_repository = MemoryRankingRepository(parser, tenant_provider)
    ranking_repository.load(rankings_dict)
    return ranking_repository


@fixture
def policy_repository() -> PolicyRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    policy_dict = {
        "default": {
            "1": Policy(id='1', name="Administrators Only", value="admin")
        }
    }
    parser = ExpressionParser()
    policy_repository = MemoryPolicyRepository(parser, tenant_provider)
    policy_repository.load(policy_dict)
    return policy_repository


@fixture
def resource_repository() -> ResourceRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    resource_dict = {
        "default": {
            "1": Resource(id='1', name="products", dominion_id="001")
        }
    }
    parser = ExpressionParser()
    resource_repository = MemoryResourceRepository(parser, tenant_provider)
    resource_repository.load(resource_dict)
    return resource_repository


@fixture
def permission_repository() -> PermissionRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    permissions_dict = {
        "default": {
            "1": Permission(id='1', resource_id='1', policy_id='1')
        }
    }
    parser = ExpressionParser()
    permission_repository = MemoryPermissionRepository(parser, tenant_provider)
    permission_repository.load(permissions_dict)
    return permission_repository


@fixture
def grant_repository() -> GrantRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    grants_dict = {
        "default": {
            "1": Grant(id='1', role_id='1', permission_id='1')
        }
    }
    parser = ExpressionParser()
    grant_repository = MemoryGrantRepository(parser, tenant_provider)
    grant_repository.load(grants_dict)
    return grant_repository


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
