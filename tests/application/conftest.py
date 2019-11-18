from typing import Dict
from pytest import fixture, raises
from authark.application.models import (
    AuthError, User, Credential, Token, Dominion, Role, Ranking,
    Policy, Resource)
from authark.application.utilities import (
    ExpressionParser, TenantProvider, StandardTenantProvider, Tenant)
from authark.application.repositories import (
    UserRepository, MemoryUserRepository,
    CredentialRepository, MemoryCredentialRepository,
    DominionRepository, MemoryDominionRepository,
    RoleRepository, MemoryRoleRepository,
    RankingRepository, MemoryRankingRepository,
    PolicyRepository, MemoryPolicyRepository,
    ResourceRepository, MemoryResourceRepository)
from authark.application.services import (
    TokenService, MemoryTokenService, AccessService,
    RefreshTokenService, ImportService, MemoryImportService)
from authark.application.coordinators import (
    AuthCoordinator, ManagementCoordinator,
    ImportCoordinator, SessionCoordinator)
from authark.application.services.hash_service import (
    HashService, MemoryHashService)


###########
# FIXTURES
###########


@fixture
def mock_user_repository() -> UserRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
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
    mock_user_repository = MemoryUserRepository(
        parser, tenant_provider)
    mock_user_repository.load(user_dict)

    return mock_user_repository


@fixture
def mock_credential_repository() -> CredentialRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    credentials_dict = {
        "default": {
            "1": Credential(id='1', user_id='1', value="HASHED: PASS1"),
            "2": Credential(id='2', user_id='2', value="HASHED: PASS2"),
            "3": Credential(id='3', user_id='3', value="HASHED: PASS3")
        }

    }
    parser = ExpressionParser()
    credential_repository = MemoryCredentialRepository(
        parser, tenant_provider)
    credential_repository.load(credentials_dict)
    return credential_repository


@fixture
def mock_dominion_repository() -> DominionRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    dominions_dict = {
        "default": {
            "1": Dominion(id='1', name='Data Server',
                          url="https://dataserver.nubark.com")
        }

    }
    parser = ExpressionParser()
    dominion_repository = MemoryDominionRepository(
        parser, tenant_provider)
    dominion_repository.load(dominions_dict)
    return dominion_repository


@fixture
def mock_role_repository() -> RoleRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    roles_dict = {
        "default": {
            "1": Role(id='1',
                      name='admin',
                      dominion_id='1',
                      description="Administrator.")
        }
    }
    parser = ExpressionParser()
    role_repository = MemoryRoleRepository(parser, tenant_provider)
    role_repository.load(roles_dict)
    return role_repository


@fixture
def mock_ranking_repository() -> RankingRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    rankings_dict = {
        "default": {
            "1": Ranking(id='1',
                         user_id='1',
                         role_id='1')
        }
    }
    parser = ExpressionParser()
    ranking_repository = MemoryRankingRepository(
        parser, tenant_provider)
    ranking_repository.load(rankings_dict)
    return ranking_repository


@fixture
def mock_policy_repository() -> PolicyRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    policy_dict = {
        "default": {
            "001": Policy(id='001', name='First Role Only', value="1")
        }
    }
    parser = ExpressionParser()
    policy_repository = MemoryPolicyRepository(
        parser, tenant_provider)
    policy_repository.load(policy_dict)
    return policy_repository


@fixture
def mock_resource_repository() -> ResourceRepository:
    tenant_provider = StandardTenantProvider(Tenant(name="Default"))
    resource_dict = {
        "default": {
            "1": Resource(id='1', name='employees', dominion_id='1')
        }
    }
    parser = ExpressionParser()
    resource_repository = MemoryResourceRepository(
        parser, tenant_provider)
    resource_repository.load(resource_dict)
    return resource_repository


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
def mock_tenant_provider() -> StandardTenantProvider:
    mock_tenant_provider = StandardTenantProvider()
    mock_tenant_provider.setup(Tenant(id='001', name='Default'))
    return mock_tenant_provider


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
                     mock_dominion_repository: DominionRepository,
                     mock_hash_service: HashService,
                     access_service: AccessService,
                     mock_refresh_token_service: RefreshTokenService
                     ) -> AuthCoordinator:
    return AuthCoordinator(mock_user_repository, mock_credential_repository,
                           mock_dominion_repository,
                           mock_hash_service, access_service,
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
def session_coordinator(
    mock_tenant_provider: TenantProvider
) -> SessionCoordinator:
    return SessionCoordinator(mock_tenant_provider)


@fixture
def access_service(mock_ranking_repository, mock_role_repository,
                   mock_dominion_repository, mock_resource_repository,
                   mock_policy_repository, mock_token_service,
                   mock_tenant_provider):
    return AccessService(
        mock_ranking_repository, mock_role_repository,
        mock_dominion_repository, mock_resource_repository,
        mock_policy_repository, mock_token_service, mock_tenant_provider)
