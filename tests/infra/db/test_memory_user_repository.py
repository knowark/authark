from pytest import fixture
from authark.app.models.user import User
from authark.app.repositories.user_repository import UserRepository
from authark.infra.db.memory_user_repository import MemoryUserRepository


def test_memory_user_repository_implementation() -> None:
    assert issubclass(MemoryUserRepository, UserRepository)


@fixture
def user_dict() -> dict:
    user_dict = {
        "ID001": User("ID001", 'Valentina', 'valenep@gmail.com'),
        "ID002": User("ID002", 'Esteban', 'tebanep@gmail.com'),
        "ID003": User("ID003", 'Gabriel', 'gabecheve@gmail.com')
    }
    return user_dict


def test_memory_user_repository_load_user(user_dict: dict) -> None:
    memory_user_repository = MemoryUserRepository()

    memory_user_repository.load(user_dict)

    assert memory_user_repository.user_dict == user_dict


def test_memory_user_repository_get_user(user_dict: dict) -> None:
    memory_user_repository = MemoryUserRepository()

    memory_user_repository.load(user_dict)
    user = memory_user_repository.get("ID001")

    assert user.uid == "ID001"
    assert user.name == "Valentina"
    assert user.email == "valenep@gmail.com"


def test_memory_user_repository_save_user() -> None:
    memory_user_repository = MemoryUserRepository()

    user = User("ID004", "Miguel", "mvp@gmail.com")

    is_saved = memory_user_repository.save(user)

    assert len(memory_user_repository.user_dict) == 1
    assert is_saved
    assert "ID004" in memory_user_repository.user_dict.keys()
    assert user in memory_user_repository.user_dict.values()
