from typing import Dict
from pytest import fixture, raises
from authark.application.coordinators.auth_coordinator import AuthCoordinator
from authark.application.repositories.user_repository import UserRepository
from authark.application.repositories.user_repository import (
    MemoryUserRepository)
from authark.application.services.token_service import (
    TokenService, MemoryTokenService)
from authark.application.services.hash_service import (
    HashService, MemoryHashService)
from authark.application.services.id_service import (
    IdService, StandardIdService)
from authark.application.models.error import AuthError
from authark.application.models.user import User
from authark.application.models.token import Token


###########
# FIXTURES
###########


@fixture
def mock_user_repository() -> UserRepository:
    MockUserRepository = MemoryUserRepository
    user_dict = {
        "valenep": User('1', 'valenep', 'valenep@gmail.com', "HASHED: PASS1"),
        "tebanep": User('2', 'tebanep', 'tebanep@gmail.com', "HASHED: PASS2"),
        "gabeche": User('3', 'gabeche', 'gabeche@gmail.com', "HASHED: PASS3")
    }
    mock_user_repository = MemoryUserRepository()
    mock_user_repository.load(user_dict)

    return mock_user_repository


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
                     mock_hash_service: HashService,
                     mock_token_service: TokenService,
                     mock_id_service: IdService) -> AuthCoordinator:
    return AuthCoordinator(mock_user_repository, mock_hash_service,
                           mock_token_service, mock_id_service)


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


def test_auth_coordinator_register(
        auth_coordinator: AuthCoordinator) -> None:

    user = auth_coordinator.register(
        "mvp", "mvp@gmail.com", "PASS4")

    assert user
    assert isinstance(user, dict)
    assert len(auth_coordinator.user_repository.user_dict) == 4
