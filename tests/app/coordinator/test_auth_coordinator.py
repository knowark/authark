from pytest import fixture
from authark.app.coordinators.auth_coordinator import AuthCoordinator
from authark.app.repositories.user_repository import UserRepository
from authark.app.models.user import User


###########
# FIXTURES
###########
@fixture
def mock_user_repository() -> UserRepository:
    # Use the in-memory repository for testing
    from authark.infra.db.memory_user_repository import MemoryUserRepository

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
def auth_coordinator(mock_user_repository: UserRepository) -> AuthCoordinator:
    return AuthCoordinator(mock_user_repository)


########
# TESTS
########
def test_auth_coordinator_creation(
        auth_coordinator: AuthCoordinator) -> None:
    assert hasattr(auth_coordinator, 'authenticate')


def test_auth_coordinator_authenticate(
        auth_coordinator: AuthCoordinator) -> None:

    authenticated = auth_coordinator.authenticate("tebanep", "PASS2")

    assert authenticated


def test_auth_coordinator_register(
        auth_coordinator: AuthCoordinator) -> None:

    user = auth_coordinator.register(
        "mvp", "mvp@gmail.com", "PASS4")

    assert user
    assert isinstance(user, User)
    assert len(auth_coordinator.user_repository.user_dict) == 4
