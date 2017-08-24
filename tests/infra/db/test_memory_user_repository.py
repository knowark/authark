from authark.app.models.user import User
from authark.app.repositories.user_repository import UserRepository
from authark.infra.db.memory_user_repository import MemoryUserRepository


def test_memory_user_repository_implementation() -> None:
    assert issubclass(MemoryUserRepository, UserRepository)


def test_memory_user_repository_load_user() -> None:
    memory_user_repository = MemoryUserRepository()

    user_list = [
        User('Esteban', 'abc'),
        User('Valen', 'xyz'),
        User('Gabriel', 'iop')
    ]

    memory_user_repository.load(user_list)

    assert memory_user_repository.user_list == user_list
