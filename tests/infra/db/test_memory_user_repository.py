from pytest import fixture
from authark.app.models.user import User
from authark.app.repositories.user_repository import UserRepository
from authark.infra.db.memory_user_repository import MemoryUserRepository


def test_memory_user_repository_implementation() -> None:
    assert issubclass(MemoryUserRepository, UserRepository)


@fixture
def user_dict() -> dict:
    user_dict = {
        "valenep": User('valenep', 'valenep@gmail.com', "PASS1"),
        "tebanep": User('tebanep', 'tebanep@gmail.com', "PASS2"),
        "gabecheve": User('gabecheve', 'gabecheve@gmail.com', "PASS3")
    }
    return user_dict


def test_memory_user_repository_load_user(user_dict: dict) -> None:
    memory_user_repository = MemoryUserRepository()

    memory_user_repository.load(user_dict)

    assert memory_user_repository.user_dict == user_dict


def test_memory_user_repository_get_user(user_dict: dict) -> None:
    memory_user_repository = MemoryUserRepository()

    memory_user_repository.load(user_dict)
    user = memory_user_repository.get("valenep")

    assert user.username == "valenep"
    assert user.email == "valenep@gmail.com"


def test_memory_user_repository_save_user() -> None:
    memory_user_repository = MemoryUserRepository()

    user = User("mvp", "mvp@gmail.com", "QWERTY")

    is_saved = memory_user_repository.save(user)

    assert len(memory_user_repository.user_dict) == 1
    assert is_saved
    assert "mvp" in memory_user_repository.user_dict.keys()
    assert user in memory_user_repository.user_dict.values()


def test_memory_user_repository_save_user_duplicate() -> None:
    memory_user_repository = MemoryUserRepository()

    user = User("mvp", "mvp@gmail.com", "QWERTY")

    is_saved = memory_user_repository.save(user)
    assert is_saved
    is_saved = memory_user_repository.save(user)
    assert not is_saved
    assert len(memory_user_repository.user_dict) == 1
