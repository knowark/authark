from typing import Dict
from pytest import fixture
from inspect import signature
from authark.application.models.user import User
from authark.application.repositories.user_repository import UserRepository
from authark.application.repositories.expression_parser import ExpressionParser
from authark.application.repositories.user_repository import (
    MemoryUserRepository)


def test_user_repository_methods() -> None:
    methods = UserRepository.__abstractmethods__
    assert 'get' in methods
    assert 'save_' in methods
    assert 'search' in methods
    assert 'delete' in methods

    sig = signature(UserRepository.save)
    assert sig.parameters.get('user')


def test_memory_user_repository_implementation() -> None:
    assert issubclass(MemoryUserRepository, UserRepository)


@fixture
def user_dict() -> Dict[str, User]:
    user_dict = {
        "1": User('1', 'valenep', 'valenep@gmail.com', "PASS1"),
        "2": User('2', 'tebanep', 'tebanep@gmail.com', "PASS2"),
        "3": User('3', 'gabeche', 'gabeche@gmail.com', "PASS3")
    }
    return user_dict


@fixture
def memory_user_repository(user_dict) -> MemoryUserRepository:
    parser = ExpressionParser()
    user_repository = MemoryUserRepository(parser)
    user_repository.load(user_dict)
    return user_repository


def test_memory_user_repository_load_user(memory_user_repository,
                                          user_dict) -> None:
    assert memory_user_repository.user_dict == user_dict


def test_memory_user_repository_get_user(memory_user_repository) -> None:
    user = memory_user_repository.get("1")

    assert user and user.username == "valenep"
    assert user and user.email == "valenep@gmail.com"


def test_memory_user_repository_save_user() -> None:
    parser = ExpressionParser()
    memory_user_repository = MemoryUserRepository(parser)

    user = User("4", "mvp", "mvp@gmail.com", "QWERTY")

    is_saved = memory_user_repository.save(user)

    assert len(memory_user_repository.user_dict) == 1
    assert is_saved
    assert "4" in memory_user_repository.user_dict.keys()
    assert user in memory_user_repository.user_dict.values()


def test_memory_user_repository_save_user_duplicate() -> None:
    parser = ExpressionParser()
    memory_user_repository = MemoryUserRepository(parser)

    user = User("4", "mvp", "mvp@gmail.com", "QWERTY")

    is_saved = memory_user_repository.save(user)
    assert is_saved
    is_saved = memory_user_repository.save(user)
    assert not is_saved
    assert len(memory_user_repository.user_dict) == 1


def test_memory_user_repository_search(memory_user_repository):
    domain = [('username', '=', "gabeche")]

    users = memory_user_repository.search(domain)

    assert len(users) == 1
    for user in users:
        assert user.id == '3'
        assert user.username == "gabeche"


def test_memory_user_repository_search_all(memory_user_repository):
    users = memory_user_repository.search([])

    assert len(users) == 3


def test_memory_user_repository_search_limit(memory_user_repository):
    users = memory_user_repository.search([], limit=2)

    assert len(users) == 2


def test_memory_user_repository_search_offset(memory_user_repository):
    users = memory_user_repository.search([], offset=2)

    assert len(users) == 1


def test_memory_user_repository_delete_user_true(memory_user_repository):
    user = memory_user_repository.user_dict["2"]
    deleted = memory_user_repository.delete(user)

    assert deleted is True
    assert len(memory_user_repository.user_dict) == 2
    assert "2" not in memory_user_repository.user_dict


def test_memory_user_repository_delete_user_false(memory_user_repository):
    user = User(**{'id': '6', 'username': 'MISSING',
                   'email': '', 'password': ''})
    deleted = memory_user_repository.delete(user)

    assert deleted is False
    assert len(memory_user_repository.user_dict) == 3
