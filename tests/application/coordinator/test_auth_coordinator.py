from typing import Dict
from pytest import fixture, raises
from authark.application.coordinators.auth_coordinator import AuthCoordinator
from authark.application.repositories.expression_parser import ExpressionParser
from authark.application.repositories.user_repository import (
    UserRepository, MemoryUserRepository)
from authark.application.repositories.credential_repository import (
    CredentialRepository, MemoryCredentialRepository)
from authark.application.services.token_service import (
    TokenService, MemoryTokenService)
from authark.application.services.hash_service import (
    HashService, MemoryHashService)
from authark.application.services.id_service import (
    IdService, StandardIdService)
from authark.application.models.error import AuthError
from authark.application.models.user import User
from authark.application.models.credential import Credential
from authark.application.models.token import Token


###########
# FIXTURES
###########


@fixture
def mock_user_repository() -> UserRepository:
    parser = ExpressionParser()
    user_dict = {
        "1": User('1', 'valenep', 'valenep@gmail.com', "HASHED: PASS1"),
        "2": User('2', 'tebanep', 'tebanep@gmail.com', "HASHED: PASS2"),
        "3": User('3', 'gabeche', 'gabeche@gmail.com', "HASHED: PASS3")
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
def mock_token_service() -> TokenService:
    mock_token_service = MemoryTokenService()
    return mock_token_service


@fixture
def mock_hash_service() -> HashService:
    mock_hash_service = MemoryHashService()
    return mock_hash_service


@fixture
def mock_id_service() -> IdService:
    mock_id_service = StandardIdService()
    return mock_id_service


@fixture
def auth_coordinator(mock_user_repository: UserRepository,
                     mock_credential_repository: CredentialRepository,
                     mock_hash_service: HashService,
                     mock_token_service: TokenService,
                     mock_id_service: IdService) -> AuthCoordinator:
    return AuthCoordinator(mock_user_repository, mock_credential_repository,
                           mock_hash_service, mock_token_service,
                           mock_id_service)


########
# TESTS
########
def test_auth_coordinator_creation(
        auth_coordinator: AuthCoordinator) -> None:
    assert hasattr(auth_coordinator, 'authenticate')


def test_auth_coordinator_authenticate(
        auth_coordinator: AuthCoordinator) -> None:

    token = auth_coordinator.authenticate("tebanep", "PASS2")

    assert isinstance(token, str)


def test_auth_coordinator_fail_to_authenticate(
        auth_coordinator: AuthCoordinator) -> None:

    with raises(AuthError):
        token = auth_coordinator.authenticate("tebanep", "WRONG_PASSWORD")


def test_auth_coordinator_fail_to_authenticate_missing_user(
        auth_coordinator: AuthCoordinator) -> None:

    with raises(AuthError):
        token = auth_coordinator.authenticate("MISSING_USER", "WRONG_PASSWORD")


def test_auth_coordinator_register(
        auth_coordinator: AuthCoordinator) -> None:

    user_dict = auth_coordinator.register(
        "mvp", "mvp@gmail.com", "PASS4")

    assert user_dict
    assert isinstance(user_dict, dict)
    assert len(auth_coordinator.user_repository.user_dict) == 4
    assert len(auth_coordinator.credential_repository.credentials_dict) == 4


def test_auth_coordinator_deregister(
        auth_coordinator: AuthCoordinator, mock_user_repository) -> None:

    user = mock_user_repository.get('2')
    unregistered = auth_coordinator.deregister(user.id)

    assert unregistered is True
    assert len(auth_coordinator.user_repository.user_dict) == 2
    assert len(auth_coordinator.credential_repository.credentials_dict) == 2


def test_auth_coordinator_deregister_missing(
        auth_coordinator: AuthCoordinator, mock_user_repository) -> None:

    user = User('5', 'missing', 'missing@gmail.com', "HASHED: MISSING")
    unregistered = auth_coordinator.deregister(user.id)

    assert unregistered is False
    assert len(auth_coordinator.user_repository.user_dict) == 3
