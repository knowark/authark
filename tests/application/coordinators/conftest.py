from typing import Dict
from pytest import fixture, raises
from authark.application.models import (
    AuthError, User, Credential, Token, Dominion, Role, Ranking,
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
    TokenService, MemoryTokenService,
    RefreshTokenService, ImportService, MemoryImportService,
    CatalogService, MemoryCatalogService,
    ProvisionService, MemoryProvisionService,
    TenantService, StandardTenantService)
from authark.application.coordinators import (
    AuthCoordinator, ManagementCoordinator, SetupCoordinator,
    ImportCoordinator, AssignmentCoordinator, AffiliationCoordinator,
    AccessCoordinator)
from authark.application.services.hash_service import (
    HashService, MemoryHashService)


###########
# FIXTURES
###########


@fixture
def mock_user_repository() -> UserRepository:
    tenant_service = StandardTenantService()
    parser = ExpressionParser()
    user_dict = {
        "default": {
            "1": User(
                id='1', username='valenep', email='valenep@gmail.com',
                external_source='erp.users', external_id='1'),
            "2": User(
                id='2', username='tebanep', email='tebanep@gmail.com',
                external_source='erp.users'),
            "3": User(
                id='3', username='gabeche', email='gabeche@gmail.com',
                external_source='erp.users', external_id='3')
        }
    }
    tenants = ['default']
    mock_user_repository = MemoryUserRepository(
        parser, tenant_service, tenants)
    mock_user_repository.load(user_dict)

    return mock_user_repository


@fixture
def mock_credential_repository() -> CredentialRepository:
    tenant_service = StandardTenantService()
    credentials_dict = {
        "default": {
            "1": Credential(id='1', user_id='1', value="HASHED: PASS1"),
            "2": Credential(id='2', user_id='2', value="HASHED: PASS2"),
            "3": Credential(id='3', user_id='3', value="HASHED: PASS3")
        }

    }
    parser = ExpressionParser()
    tenants = ['default']
    credential_repository = MemoryCredentialRepository(
        parser, tenant_service, tenants)
    credential_repository.load(credentials_dict)
    return credential_repository


@fixture
def mock_dominion_repository() -> DominionRepository:
    tenant_service = StandardTenantService()
    dominions_dict = {
        "default": {
            "1": Dominion(id='1', name='Data Server',
                          url="https://dataserver.nubark.com")
        }

    }
    parser = ExpressionParser()
    tenants = ['default']
    dominion_repository = MemoryDominionRepository(
        parser, tenant_service, tenants)
    dominion_repository.load(dominions_dict)
    return dominion_repository


@fixture
def mock_role_repository() -> RoleRepository:
    tenant_service = StandardTenantService()
    roles_dict = {
        "default": {
            "1": Role(id='1',
                      name='admin',
                      dominion_id='1',
                      description="Administrator.")
        }
    }
    parser = ExpressionParser()
    tenants = ["default"]
    role_repository = MemoryRoleRepository(parser, tenant_service, tenants)
    role_repository.load(roles_dict)
    return role_repository


@fixture
def mock_ranking_repository() -> RankingRepository:
    tenant_service = StandardTenantService()
    rankings_dict = {
        "default": {
            "1": Ranking(id='1',
                         user_id='1',
                         role_id='1')
        }
    }
    parser = ExpressionParser()
    tenants = ["default"]
    ranking_repository = MemoryRankingRepository(
        parser, tenant_service, tenants)
    ranking_repository.load(rankings_dict)
    return ranking_repository


@fixture
def mock_policy_repository() -> PolicyRepository:
    tenant_service = StandardTenantService()
    policy_dict = {
        "default": {
            "001": Policy(id='001', name='First Role Only', value="1")
        }
    }
    parser = ExpressionParser()
    tenants = ["default"]
    policy_repository = MemoryPolicyRepository(
        parser, tenant_service, tenants)
    policy_repository.load(policy_dict)
    return policy_repository


@fixture
def mock_resource_repository() -> ResourceRepository:
    tenant_service = StandardTenantService()
    resource_dict = {
        "default": {
            "1": Resource(id='1', name='employees', dominion_id='1')
        }
    }
    parser = ExpressionParser()
    tenants = ["default"]
    resource_repository = MemoryResourceRepository(
        parser, tenant_service, tenants)
    resource_repository.load(resource_dict)
    return resource_repository


@fixture
def mock_permission_repository() -> PermissionRepository:
    tenant_service = StandardTenantService()
    permission_dict = {
        "default": {
            "001": Permission(id='001', policy_id='001', resource_id='1')
        }
    }
    parser = ExpressionParser()
    tenants = ["default"]
    permission_repository = MemoryPermissionRepository(
        parser, tenant_service, tenants)
    permission_repository.load(permission_dict)
    return permission_repository


@fixture
def mock_grant_repository() -> GrantRepository:
    tenant_service = StandardTenantService()
    grants_dict = {
        "default": {
            '001': Grant(id='001', permission_id='001', role_id='1')
        }
    }
    parser = ExpressionParser()
    tenants = ["default"]
    grant_repository = MemoryGrantRepository(parser, tenant_service, tenants)
    grant_repository.load(grants_dict)
    return grant_repository


@fixture
def mock_token_service() -> TokenService:
    return MemoryTokenService()


@fixture
def mock_refresh_token_service() -> TokenService:
    return MemoryTokenService()


@fixture
def mock_hash_service() -> HashService:
    mock_hash_service = MemoryHashService()
    return mock_hash_service


@fixture
def mock_catalog_service() -> CatalogService:
    parser = ExpressionParser()
    mock_catalog_service = MemoryCatalogService(parser)
    return mock_catalog_service


@fixture
def mock_provision_service() -> ProvisionService:
    mock_provision_service = MemoryProvisionService()
    return mock_provision_service


@fixture
def mock_tenant_service() -> StandardTenantService:
    mock_tenant_service = StandardTenantService()
    return mock_tenant_service


@fixture
def mock_import_service() -> ImportService:
    mock_import_service = MemoryImportService()
    user_1 = User(**{'id': "1",
                     'external_source': "erp.users",
                     'external_id': "1",
                     'username': "pablom@test.com",
                     'email': "pablom@test.com",
                     'name': "Pablo Mendoza",
                     'gender': "male",
                     'attributes': {
                             'site_ids': ["84"]
                     }
                     }
                  )
    user_2 = User(**{'external_source': "erp.users",
                     'external_id': "2",
                     'username': "mariod@test.com",
                     'email': "mariod@test.com",
                     'name': "Mario Duarte",
                     'gender': "male",
                     'attributes': {
                             'site_ids': ["12"]
                     }
                     }
                  )
    user_4 = User(**{'external_source': "erp.users",
                     'external_id': "2",
                     'username': "mariod@test.com",
                     'email': "mariod@test.com",
                     'name': "Mario Duarte",
                     'gender': "male",
                     'attributes': {
                             'site_ids': ["12"]
                     }
                     }
                  )
    credential_1 = Credential(value="HASHED: PASS1")
    credential_2 = Credential(value="HASHED: PASS2")
    dominion_1 = Dominion(name="Data Server")
    dominion_2 = Dominion(name="User Data")
    role_1 = [[Role(name="admin"), dominion_1],
              [Role(name="user"), dominion_2]]
    users_list = [
        [user_1, credential_1, role_1], [
            user_2, None, None], [user_4, credential_2, role_1]
    ]
    mock_import_service.users = users_list
    return mock_import_service


@fixture
def auth_coordinator(mock_user_repository: UserRepository,
                     mock_credential_repository: CredentialRepository,
                     mock_hash_service: HashService,
                     access_coordinator: AccessCoordinator,
                     mock_refresh_token_service: RefreshTokenService
                     ) -> AuthCoordinator:
    return AuthCoordinator(mock_user_repository, mock_credential_repository,
                           mock_hash_service, access_coordinator,
                           mock_refresh_token_service)


@fixture
def management_coordinator(
    mock_user_repository: UserRepository,
    mock_dominion_repository: DominionRepository,
    mock_role_repository: RoleRepository,
    mock_ranking_repository: RankingRepository,
    mock_policy_repository: PolicyRepository,
    mock_resource_repository: ResourceRepository
) -> ManagementCoordinator:
    return ManagementCoordinator(
        mock_user_repository, mock_dominion_repository,
        mock_role_repository, mock_ranking_repository,
        mock_policy_repository, mock_resource_repository)


@fixture
def import_coordinator(
    mock_import_service: ImportService,
    mock_user_repository: UserRepository,
    mock_credential_repository: CredentialRepository,
    mock_role_repository: RoleRepository,
    mock_ranking_repository: RankingRepository,
    mock_dominion_repository: DominionRepository
) -> ImportCoordinator:
    return ImportCoordinator(
        mock_import_service, mock_user_repository,
        mock_credential_repository, mock_role_repository,
        mock_ranking_repository, mock_dominion_repository)


@fixture
def assignment_coordinator(
    mock_user_repository: UserRepository,
    mock_role_repository: RoleRepository,
    mock_ranking_repository: RankingRepository,
    mock_policy_repository: PolicyRepository,
    mock_resource_repository: ResourceRepository,
    mock_permission_repository: PermissionRepository,
    mock_grant_repository: GrantRepository
) -> AssignmentCoordinator:
    return AssignmentCoordinator(
        mock_user_repository, mock_role_repository,
        mock_ranking_repository,
        mock_policy_repository, mock_resource_repository,
        mock_permission_repository,
        mock_grant_repository)


@fixture
def setup_coordinator(
    mock_catalog_service: CatalogService,
    mock_provision_service: ProvisionService
) -> SetupCoordinator:
    return SetupCoordinator(
        mock_catalog_service, mock_provision_service)


@fixture
def affiliation_coordinator(
    mock_catalog_service: CatalogService,
    mock_tenant_service: TenantService
) -> AffiliationCoordinator:
    return AffiliationCoordinator(
        mock_catalog_service, mock_tenant_service)


@fixture
def access_coordinator(mock_ranking_repository, mock_role_repository,
                       mock_dominion_repository, mock_resource_repository,
                       mock_grant_repository, mock_permission_repository,
                       mock_policy_repository, mock_token_service):
    return AccessCoordinator(
        mock_ranking_repository, mock_role_repository,
        mock_dominion_repository, mock_resource_repository,
        mock_grant_repository, mock_permission_repository,
        mock_policy_repository, mock_token_service)
