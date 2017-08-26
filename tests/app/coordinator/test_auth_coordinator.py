from pytest import fixture
from authark.app.coordinators.auth_coordinator import AuthCoordinator
from authark.app.repositories.user_repository import UserRepository
from authark.app.models.user import User


@fixture
def mock_user_repository() -> UserRepository:

    class MockUserRepository(UserRepository):
        def __init__(self) -> None:
            self.user_dict = {
                "valenep": User('valenep', 'valenep@gmail.com', "PASS1"),
                "tebanep": User('tebanep', 'tebanep@gmail.com', "PASS2"),
                "gabecheve": User('gabecheve', 'gabecheve@gmail.com', "PASS3")
            }

        def get(self, username: str) -> User:
            user = self.user_dict.get(username)
            return user

        def save(self, user: User) -> bool:
            username = user.username
            self.user_dict[username] = user
            return True

    return MockUserRepository()


def test_auth_coordinator_creation(
        mock_user_repository: UserRepository) -> None:
    auth_coordinator = AuthCoordinator(mock_user_repository)
    assert hasattr(auth_coordinator, 'authenticate')


def test_auth_coordinator_authenticate(
        mock_user_repository: UserRepository) -> None:

    auth_coordinator = AuthCoordinator(mock_user_repository)

    authenticated = auth_coordinator.authenticate("tebanep", "PASS2")

    assert authenticated
