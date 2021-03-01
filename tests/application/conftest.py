from pytest import fixture
from authark.application.domain.models import (
    User, Credential, Dominion, Role, Ranking,
    Restriction, Policy)
from authark.application.domain.common import (
    QueryParser, StandardTenantProvider, Tenant,
    StandardAuthProvider, User as CUser)
from authark.application.domain.repositories import (
    UserRepository, MemoryUserRepository,
    CredentialRepository, MemoryCredentialRepository,
    DominionRepository, MemoryDominionRepository,
    RoleRepository, MemoryRoleRepository,
    RankingRepository, MemoryRankingRepository,
    RestrictionRepository, MemoryRestrictionRepository,
    PolicyRepository, MemoryPolicyRepository)
from authark.application.domain.services import (
    TokenService, MemoryTokenService, MemoryRefreshTokenService,
    RefreshTokenService, AccessTokenService, VerificationTokenService,
    MemoryVerificationTokenService, MemoryAccessTokenService,
    AccessService, VerificationService, ImportService,
    MemoryImportService, NotificationService,
    MemoryNotificationService, HashService, MemoryHashService)
from authark.application.managers import (
    AuthManager, ManagementManager, ImportManager,
    SessionManager, SecurityManager, VerificationManager)


# # ###########
# # # FIXTURES
# # ###########

@fixture
def parser():
    return QueryParser()


# PROVIDERS

@fixture
def mock_auth_provider() -> StandardAuthProvider:
    mock_auth_provider = StandardAuthProvider()
    mock_auth_provider.setup(CUser(id='001', name='johndoe'))
    return mock_auth_provider


@fixture
def mock_tenant_provider() -> StandardTenantProvider:
    mock_tenant_provider = StandardTenantProvider()
    mock_tenant_provider.setup(Tenant(id='001', name='Default'))
    return mock_tenant_provider


# # REPOSITORIES

@fixture
def mock_user_repository(mock_tenant_provider, parser) -> UserRepository:
    mock_user_repository = MemoryUserRepository(parser, mock_tenant_provider)
    mock_user_repository.load({
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
    })
    return mock_user_repository


@fixture
def mock_credential_repository(
        mock_tenant_provider, parser) -> CredentialRepository:
    mock_credential_repository = MemoryCredentialRepository(
        parser, mock_tenant_provider)
    mock_credential_repository.load({
        "default": {
            "1": Credential(id='1', user_id='1', value="HASHED: PASS1"),
            "2": Credential(id='2', user_id='2', value="HASHED: PASS2"),
            "3": Credential(id='3', user_id='3', value="HASHED: PASS3")
        }
    })
    return mock_credential_repository


@fixture
def mock_dominion_repository(
        mock_tenant_provider, parser) -> DominionRepository:
    mock_dominion_repository = MemoryDominionRepository(
        parser, mock_tenant_provider)
    mock_dominion_repository.load({
        "default": {
            "1": Dominion(id='1', name='default')
        }
    })
    return mock_dominion_repository


@fixture
def mock_restriction_repository(
        mock_tenant_provider, parser) -> RestrictionRepository:
    mock_restriction_repository = MemoryRestrictionRepository(
        parser, mock_tenant_provider)
    mock_restriction_repository.load({
        "default": {
            "1": Restriction(
                id_="1",
                group="Group name",
                name="Restriction name",
                sequence="1",
                target="Target name",
                domain="domain"
            )
        }
    })
    return mock_restriction_repository


@fixture
def mock_policy_repository(
        mock_tenant_provider, parser) -> PolicyRepository:
    mock_policy_repository = MemoryPolicyRepository(
        parser, mock_tenant_provider)
    mock_policy_repository.load({
        "default": {
            "1": Policy(
                id_="1",
                resource="Resource name",
                privilege="Privilege name",
                role="Role name",
                restriction="Restriction name",
            )
        }
    })
    return mock_policy_repository


@fixture
def mock_role_repository(mock_tenant_provider, parser) -> RoleRepository:
    mock_role_repository = MemoryRoleRepository(parser, mock_tenant_provider)
    mock_role_repository.load({
        "default": {
            "1": Role(id='1',
                      name='admin',
                      dominion_id='1',
                      description="Administrator.")
        }
    })
    return mock_role_repository


@fixture
def mock_ranking_repository(
        mock_tenant_provider, parser) -> RankingRepository:
    mock_ranking_repository = MemoryRankingRepository(
        parser, mock_tenant_provider)
    mock_ranking_repository.load({
        "default": {
            "1": Ranking(id='1', user_id='1', role_id='1'),
            "2": Ranking(id='2', user_id='2', role_id='1')
        }
    })
    return mock_ranking_repository

# # SERVICES


@fixture
def mock_token_service() -> TokenService:
    return MemoryTokenService()


@fixture
def mock_refresh_token_service() -> RefreshTokenService:
    return MemoryRefreshTokenService()

@fixture
def mock_verification_token_service() -> VerificationTokenService:
    return MemoryVerificationTokenService()


@fixture
def mock_hash_service() -> HashService:
    mock_hash_service = MemoryHashService()
    return mock_hash_service

@fixture
def mock_notification_service() -> NotificationService:
    mock_notification_service = MemoryNotificationService()
    return mock_notification_service


@fixture
def mock_import_service() -> ImportService:  # duda
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
    dominion_1 = Dominion(name="default")
    dominion_2 = Dominion(name="platformxyz")
    role_1 = [[Role(name="admin"), dominion_1],
              [Role(name="user"), dominion_2]]
    users_list = [
        [user_1, credential_1, role_1], [
            user_2, None, None], [user_4, credential_2, role_1]
    ]
    mock_import_service.users = users_list
    return mock_import_service


@fixture
def access_service(mock_ranking_repository, mock_role_repository,
                   mock_dominion_repository,
                   mock_token_service,
                   mock_tenant_provider):
    return AccessService(
        mock_ranking_repository, mock_role_repository,
        mock_dominion_repository,
        mock_token_service,
        mock_tenant_provider)


@fixture
def verification_service(
        mock_verification_token_service, mock_tenant_provider):
    return VerificationService(
        mock_verification_token_service, mock_tenant_provider)

# # COORDINATORS


@fixture
def auth_manager(mock_user_repository, mock_credential_repository,
                 mock_dominion_repository, mock_hash_service,
                 access_service, verification_service,
                 mock_notification_service, mock_refresh_token_service):
    return AuthManager(
        mock_user_repository, mock_credential_repository,
        mock_dominion_repository, mock_hash_service,
        access_service, verification_service,
        mock_notification_service, mock_refresh_token_service)


@fixture
def management_manager(
        mock_user_repository, mock_dominion_repository,
        mock_role_repository, mock_ranking_repository):
    return ManagementManager(
        mock_user_repository, mock_dominion_repository,
        mock_role_repository, mock_ranking_repository)


@fixture
def security_manager(
        mock_restriction_repository, mock_policy_repository):
    return SecurityManager(
        mock_restriction_repository, mock_policy_repository)


@fixture
def import_manager(
        mock_import_service, mock_user_repository,
        mock_credential_repository, mock_role_repository,
        mock_ranking_repository, mock_dominion_repository):
    return ImportManager(
        mock_import_service, mock_user_repository,
        mock_credential_repository, mock_role_repository,
        mock_ranking_repository, mock_dominion_repository)


@fixture
def session_manager(mock_tenant_provider, mock_auth_provider):
    return SessionManager(mock_tenant_provider, mock_auth_provider)


@fixture
def verification_manager():
    return VerificationManager()
