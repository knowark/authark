from typing import Dict
from pytest import fixture, raises
from authark.application.models import (
    AuthError, User, Credential, Token, Dominion, Role, Ranking)
from authark.application.repositories import (
    ExpressionParser,
    UserRepository, MemoryUserRepository,
    CredentialRepository, MemoryCredentialRepository,
    DominionRepository, MemoryDominionRepository,
    RoleRepository, MemoryRoleRepository,
    RankingRepository, MemoryRankingRepository)
from authark.application.services import (
    TokenService, MemoryTokenService,
    AccessService, StandardAccessService,
    ImportService, MemoryImportService)
from authark.application.coordinators import (
    AuthCoordinator, ManagementCoordinator, SetupCoordinator)
from authark.application.services.hash_service import (
    HashService, MemoryHashService)


###########
# FIXTURES
###########


@fixture
def mock_user_repository() -> UserRepository:
    parser = ExpressionParser()
    user_dict = {
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
    mock_user_repository = MemoryUserRepository(parser)
    mock_user_repository.load(user_dict)

    return mock_user_repository


@fixture
def mock_credential_repository() -> CredentialRepository:
    credentials_dict = {
        "1": Credential(id='1', user_id='1', value="HASHED: PASS1"),
        "2": Credential(id='2', user_id='2', value="HASHED: PASS2"),
        "3": Credential(id='3', user_id='3', value="HASHED: PASS3"),
    }
    parser = ExpressionParser()
    credential_repository = MemoryCredentialRepository(parser)
    credential_repository.load(credentials_dict)
    return credential_repository


@fixture
def mock_dominion_repository() -> DominionRepository:
    dominions_dict = {
        "1": Dominion(id='1', name='Data Server',
                      url="https://dataserver.nubark.com")
    }
    parser = ExpressionParser()
    dominion_repository = MemoryDominionRepository(parser)
    dominion_repository.load(dominions_dict)
    return dominion_repository


@fixture
def mock_role_repository() -> RoleRepository:
    roles_dict = {
        "1": Role(id='1',
                  name='admin',
                  dominion_id='1',
                  description="Administrator.")
    }
    parser = ExpressionParser()
    role_repository = MemoryRoleRepository(parser)
    role_repository.load(roles_dict)
    return role_repository


@fixture
def mock_ranking_repository() -> RankingRepository:
    rankings_dict = {
        "1": Ranking(id='1',
                     user_id='1',
                     role_id='1')
    }
    parser = ExpressionParser()
    ranking_repository = MemoryRankingRepository(parser)
    ranking_repository.load(rankings_dict)
    return ranking_repository


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
    role_1 = [Role(name="admin"), Role(name="user")]
    users_list = [
        [user_1, credential_1, role_1], [
            user_2, None, None], [user_4, credential_2, role_1]
    ]
    mock_import_service.users = users_list
    return mock_import_service


@fixture
def mock_access_service(mock_ranking_repository, mock_role_repository,
                        mock_dominion_repository, mock_token_service):
    return StandardAccessService(
        mock_ranking_repository, mock_role_repository,
        mock_dominion_repository, mock_token_service)


@fixture
def auth_coordinator(mock_user_repository: UserRepository,
                     mock_credential_repository: CredentialRepository,
                     mock_hash_service: HashService,
                     mock_access_service: AccessService,
                     mock_refresh_token_service: TokenService
                     ) -> AuthCoordinator:
    return AuthCoordinator(mock_user_repository, mock_credential_repository,
                           mock_hash_service, mock_access_service,
                           mock_refresh_token_service)


@fixture
def management_coordinator(
    mock_user_repository: UserRepository,
    mock_dominion_repository: DominionRepository,
    mock_role_repository: RoleRepository,
    mock_ranking_repository: RankingRepository
) -> ManagementCoordinator:
    return ManagementCoordinator(
        mock_user_repository, mock_dominion_repository,
        mock_role_repository, mock_ranking_repository)


@fixture
def setup_coordinator(
    mock_import_service: ImportService,
    mock_user_repository: UserRepository,
    mock_credential_repository: CredentialRepository,
    mock_role_repository: RoleRepository,
    mock_ranking_repository: RankingRepository
) -> SetupCoordinator:
    return SetupCoordinator(
        mock_import_service, mock_user_repository,
        mock_credential_repository, mock_role_repository,
        mock_ranking_repository)
