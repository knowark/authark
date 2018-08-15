from pytest import fixture, raises
from authark.application.models.user import User
from authark.application.repositories.user_repository import (
    UserRepository, MemoryUserRepository)
from authark.application.repositories.expression_parser import ExpressionParser
from authark.application.reporters.authark_reporter import (
    AutharkReporter, MemoryAutharkReporter)


def test_authark_reporter_methods():
    methods = AutharkReporter.__abstractmethods__
    assert 'search_users' in methods


@fixture
def user_repository() -> UserRepository:
    parser = ExpressionParser()
    user_repository = MemoryUserRepository(parser)
    user_repository.load({
        "valenep": User('1', 'valenep', 'valenep@gmail.com', "PASS1"),
        "tebanep": User('2', 'tebanep', 'tebanep@gmail.com', "PASS2"),
        "gabeche": User('3', 'gabeche', 'gabeche@gmail.com', "PASS3")
    })
    return user_repository


@fixture
def authark_reporter(user_repository) -> AutharkReporter:
    return MemoryAutharkReporter(user_repository)


def test_memory_authark_reporter_search_users_all(authark_reporter):
    domain = []
    users = authark_reporter.search_users(domain)

    assert len(users) == 3
