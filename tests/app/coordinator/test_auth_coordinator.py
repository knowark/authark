from typing import Dict
from pytest import fixture, raises
from authark.app.coordinators.auth_coordinator import AuthCoordinator
from authark.app.repositories.user_repository import UserRepository
from authark.app.repositories.user_repository import MemoryUserRepository
from authark.app.services.token_service import TokenService
from authark.app.models.error import AuthError
from authark.app.models.user import User
from authark.app.models.token import Token


###########
# FIXTURES
###########
@fixture
def mock_user_repository() -> UserRepository:
    MockUserRepository = MemoryUserRepository
    user_dict = {
        "valenep": User('valenep', 'valenep@gmail.com', "PASS1"),
        "tebanep": User('tebanep', 'tebanep@gmail.com', "PASS2"),
        "gabecheve": User('gabecheve', 'gabecheve@gmail.com', "PASS3")
    }
    mock_user_repository = MemoryUserRepository()
    mock_user_repository.load(user_dict)

    return mock_user_repository


@fixture
def mock_token_service() -> UserRepository:
    class MockTokenService(TokenService):
        def generate_token(self, payload: Dict[str, str]) -> Token:
            token = Token(b'XYZ098')
            return token

    mock_token_service = MockTokenService()

    return mock_token_service


@fixture
def auth_coordinator(mock_user_repository: UserRepository,
                     mock_token_service: TokenService) -> AuthCoordinator:
    return AuthCoordinator(mock_user_repository, mock_token_service)


########
# TESTS
########
def test_auth_coordinator_creation(
        auth_coordinator: AuthCoordinator) -> None:
    assert hasattr(auth_coordinator, 'authenticate')


def test_auth_coordinator_authenticate(
        auth_coordinator: AuthCoordinator) -> None:

    token = auth_coordinator.authenticate("tebanep", "PASS2")

    assert isinstance(token, Token)


def test_auth_coordinator_fail_to_authenticate(
        auth_coordinator: AuthCoordinator) -> None:

    with raises(AuthError):
        token = auth_coordinator.authenticate("tebanep", "WRONG_PASSWORD")


def test_auth_coordinator_register(
        auth_coordinator: AuthCoordinator) -> None:

    user = auth_coordinator.register(
        "mvp", "mvp@gmail.com", "PASS4")

    assert user
    assert isinstance(user, User)
    assert len(auth_coordinator.user_repository.user_dict) == 4
